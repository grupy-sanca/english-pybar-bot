import logging
import os
import pickle
import random
import sys

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from questions_parser import parser_list, read_file

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

questions = read_file("questions.dat")
questions = parser_list(questions)

with open("sessions.dat", "rb") as fp:
    sessions = pickle.load(fp)

TOKEN = os.getenv("TOKEN")

mode = os.getenv("MODE")
if mode == "dev":

    def run(updater):
        updater.start_polling()


elif mode == "prod":

    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))


else:
    logger.error("No MODE specified")
    sys.exit(1)


def dump_session():
    with open("sessions.dat", "wb") as fp:
        pickle.dump(sessions, fp)


def add_handler(dispatcher):
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    create_session_handler = CommandHandler("create_session", create_session)
    dispatcher.add_handler(create_session_handler)

    join_session_handler = CommandHandler("join_session", join_session)
    dispatcher.add_handler(join_session_handler)

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


def create_session(update, context):
    global sessions, questions
    session_questions = questions[:]
    random.shuffle(session_questions)
    session_id = str(update.message.from_user.id)
    sessions[session_id] = {"user_list": [session_id], "questions": session_questions}
    dump_session()

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Session created!\nUse this code to join: {session_id}"
    )


def join_session(update, context):
    global sessions
    text_split = update.message.text.split()
    if len(text_split) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Usage: /join_session SESSION_ID")
        return
    session_id = text_split[-1]
    if session_id not in sessions.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"SESSION_ID {session_id} is invalid")
        return
    user = update.message.from_user.id
    if user in sessions[session_id]["user_list"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"You already are in this session!")
        return

    sessions[session_id]["user_list"].append(user)
    dump_session()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Session joined!\nThe current questions is: {sessions[session_id]['questions'][-1]}",
    )


if __name__ == "__main__":
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    add_handler(dispatcher)
    run(updater)
