from typing import Iterable

import telebot
from logging import Handler, LogRecord


class TelegramBotHandler(Handler):
    def __init__(self, token: str, admin_chat_ids: Iterable[str]):
        super().__init__()
        self.token = token
        self.admin_chat_ids = admin_chat_ids

    def emit(self, record: LogRecord):
        bot = telebot.TeleBot(self.token)
        for chat_id in self.admin_chat_ids:
            bot.send_message(
                chat_id,
                self.format(record)
            )