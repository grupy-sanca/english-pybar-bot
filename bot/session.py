import pickle
import random

class Session:
    def __init__(self, file_path):
        self.file_path = file_path


    def load_session(self):
        with open(self.file_path, "rb") as fp:
            self.sessions = pickle.load(fp)

    def dump_session(self):
        with open(self.file_path, "wb") as fp:
            pickle.dump(self.sessions, fp)

    def set_questions(self, questions):
        self.questions = questions

    def start_session(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Hello World!"
        )

    def create_session(self, update, context):
        session_id = str(update.message.from_user.id)
        self.sessions[session_id] = {"user_list": [session_id], "questions": random.shuffle(self.questions[:])}
        self.dump_session()

        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Session created!\nUse this code to join: {session_id}"
        )

    def join_session(self, update, context):
        text_split = update.message.text.split()
        if len(text_split) < 2:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"Usage: /join_session SESSION_ID"
            )
            return
        session_id = text_split[-1]
        if session_id not in self.sessions.keys():
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"SESSION_ID {session_id} is invalid"
            )
            return
        user = update.message.from_user.id
        if user in self.sessions[session_id]["user_list"]:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"You already are in this session!"
            )
            return

        self.sessions[session_id]["user_list"].append(user)
        self.dump_session()

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Session joined!\nThe current questions is:\n{self.sessions[session_id]['questions'][-1]}",
        )

    def get_session_id(self, user):
        for session_id, session in self.sessions.items():
            if user in session["user_list"]:
                return session_id

    def session_draw_question(self, update, context):
        user = update.message.from_user.id
        session_id = self.get_session_id(user)

        if not session_id:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=random.choice(self.questions)
            )
            return
        if not self.sessions[session_id]["questions"]:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Questions list is empty :("
            )
            return
        self.sessions[session_id]["questions"].pop()
        self.dump_session()
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{self.sessions[session_id]['questions'][-1]}"
        )

    def current_session_question(self, update, context):
        user = update.message.from_user.id
        session_id = self.get_session_id(user)

        if not session_id:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="You currently don't belong to a session"
            )
            return

        if not self.sessions[session_id]["questions"]:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Questions list is empty :("
            )
            return

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"The current question is:\n{sessions[session_id]['questions'][-1]}",
        )
