from data_manager import QUESTIONS

# TODO: This function does not work

def find_answers_by_question(question_id, answers_file) -> list :
    return [single_answer for single_answer in answers_file if int(single_answer["question_id"]) == int(question_id)]
