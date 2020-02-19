import connection

# TODO: We need csv file HEADER, to print (display) table headers for questions and answers

QUESTION_FILE_PATH = "sample_data/question.csv"
ANSWERS_FILE_PATH = "sample_data/answer.csv"

QUESTIONS = connection.open_file(QUESTION_FILE_PATH)
ANSWERS = connection.open_file(ANSWERS_FILE_PATH)


