import logging
import os
import random

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from questions_parser import parser_list, read_file

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

questions = read_file("questions.dat")
questions = parser_list(questions)


def main(token):
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    add_handler(dispatcher)
    updater.start_polling()


def add_handler(dispatcher):
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    message_handler = MessageHandler(Filters.text, send_message)
    dispatcher.add_handler(message_handler)


def send_message(update, context):
    logger.info(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=draw_question())


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello World!")


def draw_question():
    global questions
    return random.choice(questions)


if __name__ == "__main__":
    token = os.environ["TOKEN"]
    main(token)
