import connection

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
    query = f""" SELECT * FROM {table_name};"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@connection.connection_handler
def update_data_in_table(cursor, table_name, data_to_update, condition):

    update_query = f"""UPDATE {table_name} SET """

    if len(data_to_update.keys())>1:
        for key,value in data_to_update.items():
            update_query += f"{key[0]} = %({key[0]})s, "
        update_query.rstrip(",")
    else:
        update_query += f"{list(data_to_update.keys())[0]} = %({list(data_to_update.keys())[0]})s "

    update_query += f"WHERE {list(condition.keys())[0]} = %({list(condition.keys())[0]})s;"

    data_to_update.update(condition)
    cursor.execute(update_query, data_to_update)

