import connection

QUESTION_FILE_PATH = "sample_data/question.csv"
ANSWER_FILE_PATH = "sample_data/question.csv"

QUESTIONS_DICT = connection.open_file(QUESTION_FILE_PATH)
print(QUESTIONS_DICT)