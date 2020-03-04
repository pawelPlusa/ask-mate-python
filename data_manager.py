import connection

# TODO: Remove
QUESTION_FILE_PATH = "sample_data/question.csv"
ANSWERS_FILE_PATH = "sample_data/answer.csv"

QUESTIONS = connection.open_file(QUESTION_FILE_PATH)
ANSWERS = connection.open_file(ANSWERS_FILE_PATH)


#just a template for further functions

@connection.connection_handler
def get_mentor_names_by_first_name(cursor, first_name):
    cursor.execute("""
                    SELECT first_name, last_name FROM mentors
                    WHERE first_name = %(a)s ORDER BY first_name;
                   """,
                   {'a': first_name})
    names = cursor.fetchall()
    return names


@connection.connection_handler
def get_all_from_given_table(cursor, table_name: str):

    query = f"""SELECT * FROM {table_name};"""
    cursor.execute(query)
    result = cursor.fetchall()

    return result


@connection.connection_handler
def update_data_in_table(cursor, table_name: str, data_to_update: dict, condition: dict):

    update_query = f"""UPDATE {table_name} SET """
    for key in data_to_update:
        update_query += f"""{key} = %({key})s, """
    update_query = update_query.rstrip(", ")

    update_query += f""" WHERE {next(iter(condition))} = %({next(iter(condition))})s;"""
    data_to_update.update(condition)

    # print(update_query)
    # print(f"cmfff {cursor.mogrify(update_query, data_to_update)}")
    cursor.execute(update_query, data_to_update)
    # print(cursor.query)


# TODO: Finish delete - Pawel

@connection.connection_handler
def delete_data_in_table(cursor, table_name, condition):

    update_query = f"""DELETE FROM {table_name} """
    update_query += f"""WHERE {list(condition.keys())[0]} = %({list(condition.keys())[0]})s;"""

    data_to_update.update(condition)
    cursor.execute(update_query, data_to_update)

    cursor.execute(update_query, condition)

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
    cursor.execute(insert_query,data_to_insert)
