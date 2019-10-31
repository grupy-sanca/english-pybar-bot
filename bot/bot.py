import os
import sys
from dotenv import load_dotenv
from questions import Question
from session import Session
from log import Log
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

def get_file_path(path):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    return os.path.join(fileDir, path)

def add_handler(dispatcher, name, func):
    handler = CommandHandler(name, func)
    dispatcher.add_handler(handler)

def send_message(update, context):
    logger.info(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=draw_question())


file_path = get_file_path('../local.env')
load_dotenv(file_path)
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
    logger.log_error("No MODE specified")

def main():
    path = get_file_path('../static/questions.dat')
    questions = Question(path)
    questions.read_file()
    questions.parse_file()

    path = get_file_path('../static/sessions.dat')
    session = Session(path)
    session.load_session()
    session.set_questions(questions)

    logger = Log()


if __name__ == "__main__":

    main()
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    add_handler(dispatcher, "start", session.start_session)
    add_handler(dispatcher, "create_session", session.create_session)
    add_handler(dispatcher, "join_session", session.join_session)
    add_handler(dispatcher, "session_draw_question", session.session_draw_question)
    add_handler(dispatcher, "current_session_question", session.current_session_question)
    dispatcher.add_handler(MessageHandler(Filters.text, send_message))
    run(updater)
