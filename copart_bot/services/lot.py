import asyncio
import datetime
import logging

import aiohttp
from sqlalchemy import select, update, bindparam
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from copart_bot.models import Lot, Chat
from copart_bot.services.chat import ChatService
from copart_bot.utils import convert_timestamp_to_datetime

logger = logging.getLogger(__name__)


class LotService:

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_or_create_lot(session: AsyncSession, lot_id):
        lot_id = int(lot_id)
        result = await session.scalars(
            select(Lot).where(
                Lot.lot_id == lot_id
            ).options(selectinload(Lot.chats))
        )
        lot = result.one_or_none()
        if lot:
            return lot
        lot = Lot(lot_id=lot_id)
        session.add(lot)
        return lot

    async def create_lot_for_chat(self, session: AsyncSession, lot_id, chat_id):
        chat = await ChatService.get_chat(session, chat_id=chat_id)
        lot = await LotService.get_or_create_lot(session, lot_id)

        try:
            lot.chats.append(chat)
        except IntegrityError as ex:
            await self.bot.send_message(chat_id, 'You already watch this lot')

        try:
            await session.commit()
            return lot
        except IntegrityError as ex:
            print('Create lot error. Rolling back')
            print(ex)
            await self.bot.send_message(chat_id, 'Server error occured')
            await session.rollback()

    async def remove_lot_for_chat(self, session: AsyncSession, lot_id, chat_id):
        chat = await ChatService.get_chat(session, chat_id=chat_id)
        lot = await LotService.get_or_create_lot(session, lot_id)

        try:
            lot.chats.remove(chat)
        except IntegrityError as ex:
            await self.bot.send_message(chat_id, 'You are not watching this lot!')

        try:
            await session.commit()
            return lot
        except IntegrityError as ex:
            logger.error(ex)
            await self.bot.send_message(chat_id, 'Server error occured')
            await session.rollback()

    @staticmethod
    async def get_lot_auction_date(lot_id):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
            'Accept-Language': 'en-GB,en;q = 0.9',
            'Accept-Encoding': 'gzip,deflate,br',
            'Connection': 'keep-alive',
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                    f'https://www.copart.com/public/data/lotdetails/solr/{lot_id}') as resp:
                try:
                    data = await resp.json()
                    auction_date = convert_timestamp_to_datetime(
                        data.get('data', {}).get('lotDetails', {}).get('ad')
                    )

                    return auction_date
                except Exception as e:
                    logger.error(e)

    @staticmethod
    async def get_empty_lots(session):
        result = await session.scalars(
            select(Lot).where(
                Lot.auction_date == 0
            ).options(selectinload(Lot.chats))
        )
        return result.all()

    async def notify_about_lot(self, lot, auction_date):
        for chat in lot.chats:
            await self.bot.send_message(
                chat.chat_id,
                f'Lot {lot.lot_id} has now assigned auction date: {auction_date}'
            )

    async def check_new(self, session):
        lots = await self.get_empty_lots(session)
        lots_to_update = []
        for lot in lots:

            auction_date = await self.get_lot_auction_date(lot.lot_id)
            if auction_date is not None:
                await self.notify_about_lot(lot, auction_date)
            else:
                await asyncio.sleep(10)
        if lots_to_update:
            stmt = (
                update(Lot)
                .where(Lot.id == bindparam("_id"))
                .values(auction_date=bindparam("auction_date"))
            )
            connection = await session.connection()
            await connection.execute(stmt, lots_to_update)
            await connection.commit()
