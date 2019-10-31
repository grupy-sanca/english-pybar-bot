import random

class Question:

    def __init__(self, file_path):
        self.file_path = file_path
        self.questions = []

    def read_file(self):
        with open(self.file_path) as file:
            self.questions = file.read().split("|")

    def parse_file(self):
        return [question.strip() for question in self.questions if question.strip()]


