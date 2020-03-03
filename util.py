'''
This module defines additional functions.
'''

import time
import copy


def find_answers_by_question(question_id: str, answers_file: list) -> list:
    """
    Finds answers(list) for selected question_id
    param: question_id: str
    param: answers_file: list
    returns list of answers: list
    if there is no question with given id, returns empty list
    """

    return [single_answer for single_answer in answers_file if single_answer["question_id"] == question_id]


def change_time_format(datafile):
    """
    Takes list of dics and changes time format for more human friendly.
    Should be used only when passing data to html
    """
    datafile_with_dates = copy.deepcopy(datafile)
    # for single_dict in datafile_with_dates:
        # print(single_dict)
        # single_dict["submission_time"] = time.strftime("%d %m %Y, %H:%M",
        #                                                time.localtime(int(single_dict["submission_time"])))
    return datafile_with_dates


def find_next_id(contents_list: list) -> str:
    """
    Finds new id
    param: contents_list: list of dicts
    returns id: str
    """

    number = 0
    contents_list.sort(key=lambda item: int(item['id']))
    while number < len(contents_list):
        if contents_list[number]['id'] != str(number):
            return str(number)
        number += 1
    return str(number)


def find_index_of_dict_by_id(dict_list, given_id):
    index_number = 0
    for dictionary in dict_list:
        if dictionary["id"] == given_id:
            return index_number

        index_number += 1
    return None


def get_single_row(data, searched_id):
    """ takes single row from database """
    return [row for row in data if row["id"] == int(searched_id)][0]


def purge_answer_list(answers, question_id):
    """
    Takes a list of dictionaries and returns other
    list without those related to given question_id
    """

    purged_answers = []
    for answer in answers:
        if answer["question_id"] != str(question_id):
            purged_answers.append(answer)
    return purged_answers
