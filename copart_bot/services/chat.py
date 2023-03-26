from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from copart_bot.models import Chat


class ChatService:

    @staticmethod
    async def create_user(session: AsyncSession, chat_id, name):
        chat = Chat(chat_id=chat_id, name=name, lots=[])
        session.add(chat)
        try:
            await session.commit()
            return chat
        except IntegrityError as ex:
            print('Create chat error. Rolling back')
            await session.rollback()

    @staticmethod
    async def get_chat(session: AsyncSession, chat_id):
        result = await session.execute(select(Chat).where(Chat.chat_id == chat_id))
        chat = result.scalars().first()
        return chat
