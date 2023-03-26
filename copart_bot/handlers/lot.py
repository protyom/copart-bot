from telegram import Update
from telegram.ext import ContextTypes

from copart_bot.services.lot import LotService


async def lot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        lot_id = context.args[0]
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Send lot_id after lot (i.e. /lot <lot_id>)")
        return

    auction_date = await LotService.get_lot_auction_date(lot_id)
    message = 'This lot has no auction date'
    if auction_date:
        message = f'The auction is on {auction_date}'
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=message)
