from telegram import Update
from telegram.ext import ContextTypes


from copart_bot.db import async_session
from copart_bot.services.lot import LotService


async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = LotService(bot=context.bot)

    try:
        lot_id = context.args[0]
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Send lot_id after lot (i.e. /watch <lot_id>)")
        return

    auction_date = await LotService.get_lot_auction_date(lot_id)
    if auction_date:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='This lot already has assigned auction')
        return
    async with async_session() as session:
        created_lot = await service.create_lot_for_chat(session, lot_id,
                                                           update.effective_chat.id)
        if created_lot:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Lot is now being watched. If an ad will appear you will be notified.')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Server error. Please contact developers')

