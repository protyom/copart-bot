import os

from telegram.ext import ApplicationBuilder, CommandHandler

from copart_bot.handlers import start, lot, watch, unwatch
from copart_bot.jobs import callback_check
import copart_bot.logger.conf


BOT_TOKEN = os.environ.get('BOT_TOKEN')
application = ApplicationBuilder().token(BOT_TOKEN).build()

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)
lot_handler = CommandHandler('lot', lot)
application.add_handler(lot_handler)

watch_handler = CommandHandler('watch', watch)
application.add_handler(watch_handler)
unwatch_handler = CommandHandler('unwatch', unwatch)
application.add_handler(unwatch_handler)


# JOBS
job_queue = application.job_queue
job_queue.run_repeating(callback_check, first=5, interval=3600)
