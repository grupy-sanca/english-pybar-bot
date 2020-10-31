import logging
import os
import pickle
import random
import sys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater

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

    help_handler = CommandHandler("help", help)
    dispatcher.add_handler(help_handler)

    create_session_handler = CommandHandler("create_session", create_session)
    dispatcher.add_handler(create_session_handler)

    join_session_handler = CommandHandler("join_session", join_session)
    dispatcher.add_handler(join_session_handler)

    session_draw_question_handler = CommandHandler("session_draw_question", session_draw_question)
    dispatcher.add_handler(session_draw_question_handler)

    current_session_question_handler = CommandHandler("current_session_question", current_session_question)
    dispatcher.add_handler(current_session_question_handler)

    message_handler = MessageHandler(Filters.text, send_message)
    dispatcher.add_handler(message_handler)


def send_message(update, context):
    logger.info(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=draw_question())


def help(update, context):
    text = "Welcome to the English PyBar Bot by @grupysanca!\n\n"
    text += "Send /start to get started.\n\n"
    text += "To create a new session, click on the 'Create session' button.\n\n"
    text += "You can get a random question from the default question list without joining a session clicking on the 'Draw random question' button.\n\n"
    text += "If you already have a session id, send /join_session SESSION_ID to join.\n\n"
    text += (
        "Once you join a session, there are buttons to draw a new question and to get the current one.\n\n"
    )
    text += "Have fun!\n\n"
    text += "This bot is open source and can be found here: https://github.com/grupy-sanca/english-pybar-bot"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Create session", callback_data="/create_session"),
            InlineKeyboardButton("Draw random question", callback_data="/random_question"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Hello World!\nPlease, create a new session or draw a random question", reply_markup=reply_markup
    )


def on_button_press(update, context):
    query = update.callback_query
    query.answer()

    if "/create_session" in query.data:
        create_session(query, context)
        return
    if "/draw_question" in query.data:
        session_draw_question(query, context)
        return
    if "/current_question" in query.data:
        current_session_question(query, context)
        return
    if "/random_question" in query.data:
        keyboard = [[InlineKeyboardButton("Draw random question", callback_data="/random_question")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"Random question:\n{draw_question()}", reply_markup=reply_markup)
        return

    query.edit_message_text(text=f"Selected: {query.data}")


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

    update.edit_message_text(text=f"Session created!\nUse this code to join: {session_id}")


def join_session(update, context):
    global sessions
    text_split = update.message.text.split()
    if len(text_split) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /join_session SESSION_ID")
        return
    session_id = text_split[-1]
    if session_id not in sessions.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"SESSION_ID {session_id} is invalid")
        return
    user = update.message.from_user.id
    if user in sessions[session_id]["user_list"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You already are in this session!")
        return

    sessions[session_id]["user_list"].append(user)
    dump_session()

    keyboard = [
        [
            InlineKeyboardButton("Draw next question", callback_data="/draw_question"),
            InlineKeyboardButton("Get current question", callback_data="/current_question"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Session joined!\nThe current questions is:\n{sessions[session_id]['questions'][-1]}",
        reply_markup=reply_markup,
    )


def get_session_id(user):
    global sessions
    session_id = None
    for session_id, session in sessions.items():
        if user in session["user_list"]:
            session_id = session_id
            break
    return session_id


def session_draw_question(update, context):
    global sessions
    user = update.message.from_user.id
    session_id = get_session_id(user)

    if not session_id:
        update.edit_message_text(text=f"You're not in a session.\nRandom question:\n{draw_question()}")
        return
    if not sessions[session_id]["questions"]:
        update.edit_message_text(text="Questions list is empty :(")
        return
    sessions[session_id]["questions"].pop()
    dump_session()

    keyboard = [
        [
            InlineKeyboardButton("Draw next question", callback_data="/draw_question"),
            InlineKeyboardButton("Get current question", callback_data="/current_question"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.edit_message_text(
        text=f"The next question is:\n{sessions[session_id]['questions'][-1]}", reply_markup=reply_markup
    )


def current_session_question(update, context):
    global sessions
    user = update.message.from_user.id
    session_id = get_session_id(user)

    if not session_id:
        update.edit_message_text(text="You currently don't belong to a session")
        return
    if not sessions[session_id]["questions"]:
        update.edit_message_text(text="Questions list is empty :(")
        return

    keyboard = [
        [
            InlineKeyboardButton("Draw next question", callback_data="/draw_question"),
            InlineKeyboardButton("Get current question", callback_data="/current_question"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.edit_message_text(
        text=f"The current question is:\n{sessions[session_id]['questions'][-1]}", reply_markup=reply_markup
    )


if __name__ == "__main__":
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    add_handler(dispatcher)

    dispatcher.add_handler(CallbackQueryHandler(on_button_press))

    run(updater)
