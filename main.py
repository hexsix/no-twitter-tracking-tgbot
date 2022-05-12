from doctest import NORMALIZE_WHITESPACE
import logging
import os
import re

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters


TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", "8443"))


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=
            "The only thing I can do is getting rid of twitter tracking code tails\n"
            "\n"
            "For example, https://twitter.com/daguguguji/status/114514?t=1919810&s=19 to https://twitter.com/daguguguji/status/114514 \n"
            "Or, https://twitter.com/daguguguji/status/114514/photo/1 to https://twitter.com/daguguguji/status/114514 \n"
            "\n"
            "If you find any bugs, please stop using and open an issue on \n"
            "https://github.com/hexsix/no-twitter-tracking-tgbot"
        )


def replace(text):
    match = re.search(r"https:\/\/(?:www\.)?twitter\.com\/(\w){1,15}\/status\/(\d)*\S*", text)
    if match:
        src = match.group()
        dst = re.search(r"https:\/\/(?:www\.)?twitter\.com\/(\w){1,15}\/status\/(\d)*", src).group()
        return text.replace(src, dst)
    else:
        return None


def no_twitter_tracking_text(update, context):
    text = replace(update.channel_post.text)
    if not text:
        return
    context.bot.editMessageText(chat_id=update.channel_post.chat_id,
                                message_id=update.channel_post.message_id,
                                text=text)


def no_twitter_tracking_caption(update, context):
    caption = replace(update.channel_post.caption)
    if not caption:
        return
    context.bot.editMessageCaption(chat_id=update.channel_post.chat_id,
                                   message_id=update.channel_post.message_id,
                                   caption=caption)


def error(update, context):
    logger.warning(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    no_twitter_tracking_txt_handler = MessageHandler(Filters.text & Filters.update.channel_post, no_twitter_tracking_text)
    no_twitter_tracking_caption_handler = MessageHandler(Filters.caption & Filters.update.channel_post, no_twitter_tracking_caption)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(no_twitter_tracking_txt_handler)
    dispatcher.add_handler(no_twitter_tracking_caption_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
