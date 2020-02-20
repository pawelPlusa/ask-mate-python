'''
This module defines additional functions.
'''

import time
import data_manager
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
    for single_dict in datafile_with_dates:
        single_dict["submission_time"] = time.strftime("%d %m %Y, %H:%M",
                                                       time.localtime(int(single_dict["submission_time"])))
    return datafile_with_dates


def find_next_id(contents_list: list) -> str:
    """
    Finds new id
    param: contents_list: list of dicts
    returns id: str
    """

    number = 0
    while number < len(contents_list):
        if contents_list[number]['id'] != str(number):
            return str(number)
        number += 1
    return str(number)

