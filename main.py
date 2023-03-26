import argparse
import asyncio
import logging

from copart_bot.db import init_models
from copart_bot.application import application

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DB initialization')
    parser.add_argument('--init_db', default=False, action='store_true')
    arguments_parsed = parser.parse_args()
    if arguments_parsed.init_db:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init_models())
        loop.close()

    application.run_polling()
