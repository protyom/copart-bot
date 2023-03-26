import logging.config
import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },

    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'telegram_handler': {
            'class': 'copart_bot.logger.handlers.TelegramBotHandler',
            'admin_chat_ids': [os.environ.get('TELEGRAM_ADMIN_ID')],
            'token': os.environ.get('TELEGRAM_ERROR_BOT_TOKEN'),
            'formatter': 'default_formatter',
        }
    },

    'loggers': {
        'copart_bot.services.lot': {
            'handlers': ['stream_handler', 'telegram_handler'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
