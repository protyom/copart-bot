from telegram import Update
from telegram.ext import ContextTypes


from copart_bot.db import async_session
from copart_bot.services.lot import LotService


async def unwatch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = LotService(bot=context.bot)

    try:
        lot_id = context.args[0]
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Send lot_id after lot (i.e. /unwatch <lot_id>)")
        return

    async with async_session() as session:
        created_lot = await service.remove_lot_for_chat(session, lot_id,
                                                           update.effective_chat.id)
        if created_lot:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Lot has been removed from watched.')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Server error. Please contact developers')

