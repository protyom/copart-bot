from telegram import Update
from telegram.ext import ContextTypes


from copart_bot.db import async_session
from copart_bot.services.chat import ChatService



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with async_session() as session:
        chat = await ChatService.create_user(session=session,
                                             chat_id=update.effective_chat.id,
                                             name=update.effective_chat.effective_name)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hello! Send me /lot <lot_id> and I'll check lot info.")
