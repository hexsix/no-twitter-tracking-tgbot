from doctest import NORMALIZE_WHITESPACE
import logging
import os
import re

from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters


TOKEN = os.getenv("TOKEN")
TOKEN = "5394366887:AAG_5NKQ6HoAb2oPCM3usOmzn-IJlUiEnBU"
DST = re.compile(r"https:\/\/(?:www\.)?twitter\.com\/(\w){1,15}\/status\/(\d)*")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=
            "The only thing I can do\n"
            "is getting rid of twitter tracking code tails\n"
            "\n"
            "For example, https://twitter.com/daguguguji/status/114514?t=1919810&s=19 \n"
            "to https://twitter.com/daguguguji/status/114514 \n"
            "\n"
            "If you find any bugs, please stop using and open an issue on \n"
            "https://github.com/hexsix/no-twitter-tracking-tgbot"
        )


def replace(text: str) -> (str|None):
    match = re.search(r"https:\/\/(?:www\.)?twitter\.com\/(\w){1,15}\/status\/(\d)*\?t=(\w)*&s=(\d){1,2}", text)
    if match:
        src = match.group()
        dst = re.search(r"https:\/\/(?:www\.)?twitter\.com\/(\w){1,15}\/status\/(\d)*", src).group()
        return text.replace(src, dst)
    else:
        return None


def no_twitter_tracking_text(update: Update, context: CallbackContext):
    text = replace(update.message.text)
    if not text:
        return
    context.bot.editMessageText(chat_id=update.message.chat_id,
                                message_id=update.message.reply_to_message.message_id,
                                text=text)


def no_twitter_tracking_caption(update: Update, context: CallbackContext):
    caption = replace(update.message.caption)
    if not caption:
        return
    context.bot.editMessageCaption(chat_id=update.message.chat_id,
                                   message_id=update.message.reply_to_message.message_id,
                                   caption=caption)


if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    no_twitter_tracking_handler = MessageHandler(Filters.text & (~Filters.command), no_twitter_tracking_text)
    no_twitter_tracking_handler = MessageHandler(Filters.caption & (~Filters.command), no_twitter_tracking_caption)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(no_twitter_tracking_handler)

    updater.start_polling()
