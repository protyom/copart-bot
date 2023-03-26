from telegram.ext import ContextTypes, Application

from copart_bot.db import async_session
from copart_bot.services.lot import LotService


async def callback_check(context: ContextTypes.DEFAULT_TYPE):
    service = LotService(bot=context.bot)
    async with async_session() as session:
        await service.check_new(session)
