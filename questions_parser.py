def read_file(file_path):
    with open(file_path) as file:
        return file.read().split("|")

def parser_list(questions):
    return [question.strip() for question in questions if question.strip()]


