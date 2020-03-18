"""
This module defines additional functions.
"""

import copy, data_manager, bcrypt

"""
FUNCTIONS FROM SPRINT#3
"""

def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

"""
FUNCTIONS FROM SPRINT#2
"""
def check_if_vote(table, id, vote):

    sql_condition = {"id": int(id)}
    row_to_edit = data_manager.get_from_table_condition(table, sql_condition)[0]
    votes_no = int(row_to_edit["vote_number"])
    if vote == "vote_down":
        votes_no -= 1
    elif vote == "vote_up":
        votes_no += 1
    data_to_update = {"vote_number" : str(votes_no)}
    data_manager.update_data_in_table(table, data_to_update, sql_condition)


"""
FUNCTIONS FROM SPRINT#1
"""
def change_time_format(datafile):
    """
    Takes list of dicts and changes time format for more human friendly.
    Should be used only when passing data to html
    """
    datafile_with_dates = copy.deepcopy(datafile)

    if type(datafile_with_dates) != list:
        list(datafile_with_dates)


    for single_dict in datafile_with_dates:
        single_dict["submission_time"] = single_dict["submission_time"].strftime("%d %m %Y, %H:%M")

    return datafile_with_dates


def proper_capitalization(string):

    return string[0].capitalize() + string[1:] if string else ""
