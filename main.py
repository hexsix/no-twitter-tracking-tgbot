import logging
import os
import re

from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, Filters


TOKEN = os.getenv("TOKEN")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def help(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=
              "The only thing I can do\n"
              "is getting rid of twitter tracking code tails\n"
              "\n"
              "For example, https://twitter.com/daguguguji/status/114514?t=1919810&s=19 \n"
              "to https://twitter.com/daguguguji/status/114514 \n"
              "\n"
              "If you find any bugs, please stop using and open an issue on \n"
              "https://github.com/hexsix/no-twitter-tracking-tgbot"
          )


async def no_twitter_tracking(update: Update, context: CallbackContext):
    await context.bot.editMessageText(chat_id=update.message.chat_id,
                                      message_id=update.message.reply_to_message.message_id,
                                      text="edited")


if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    no_twitter_tracking_handler = MessageHandler(Filters.all, no_twitter_tracking)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(no_twitter_tracking_handler)

    application.run_polling()
