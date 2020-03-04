import connection
import copy

QUESTION_FILE_PATH = "sample_data/question.csv"
ANSWERS_FILE_PATH = "sample_data/answer.csv"

QUESTIONS = connection.open_file(QUESTION_FILE_PATH)
ANSWERS = connection.open_file(ANSWERS_FILE_PATH)



#just a template for further functions
@connection.connection_handler
def get_mentor_names_by_first_name(cursor, first_name):
    cursor.execute("""
                    SELECT first_name, last_name FROM mentors
                    WHERE first_name = %(first_name)s ORDER BY first_name;
                   """,
                   {'first_name': first_name})
    names = cursor.fetchall()
    return names


@connection.connection_handler
def get_all_from_given_table(cursor, table_name):
    """
    :rtype: list of dicts
    """
    query = f""" SELECT * FROM {table_name};"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@connection.connection_handler
def get_from_table_condition(cursor, table_name, condition: dict):
    """
    :rtype: list of dicts
    """
    query = f""" SELECT * FROM {table_name} WHERE {next(iter(condition))} = %({next(iter(condition))})s;"""

    cursor.execute(query, condition)
    result = cursor.fetchall()
    return result

@connection.connection_handler
def update_data_in_table(cursor, table_name: str, data_to_update: dict, condition: dict):
    """
    Takes table_name, data_to_update as a list of dicts, and condition to
    create sql update query. Cursor is added by decorator f.
    :param cursor:
    :param table_name:
    :param data_to_update:
    :param condition:
    :return: No return
    """
    update_query = f"""UPDATE {table_name} SET """
    for key in data_to_update.keys():
        update_query += f"{key} = %({key})s, "
    update_query = update_query.rstrip(", ")

    update_query += f" WHERE {list(condition.keys())[0]} = %({list(condition.keys())[0]})s;"
    data_to_update.update(condition)

    # print(update_query)
    # print(f"cmfff {cursor.mogrify(update_query, data_to_update)}")
    cursor.execute(update_query, data_to_update)
    # print(cursor.query)


#TODO: Finish delete - Pawel
@connection.connection_handler
def delete_data_in_table(cursor, table_name, condition):

    update_query = f"""DELETE FROM {table_name} """
    update_query += f"WHERE {list(condition.keys())[0]} = %({list(condition.keys())[0]})s;"

    # print(update_query)
    print(f"cmfff {cursor.mogrify(update_query, condition)}")
    # cursor.execute(update_query, condition)
    # print(cursor.query)
    return None


@connection.connection_handler
def insert_data_to_table(cursor, table_name, data_to_insert):

    insert_query = f"INSERT INTO {table_name} ("
    for key in data_to_insert.keys():
        insert_query += f"{key}, "
    insert_query = ")".join(insert_query.rsplit(", ", 1))

    insert_query += f" VALUES ("
    for key in data_to_insert.keys():
        insert_query += f"%({key})s, "
    insert_query = ")".join(insert_query.rsplit(", ", 1))
    # print(insert_query)
    # print(cursor.mogrify(insert_query,data_to_insert))
    cursor.execute(insert_query,data_to_insert)