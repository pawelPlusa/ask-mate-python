import connection


@connection.connection_handler
def get_all_from_given_table(cursor, table_name: str):

    query = f"""SELECT * FROM {table_name};"""
    cursor.execute(query)
    result = cursor.fetchall()

    return result


@connection.connection_handler
def get_from_table_condition_like(cursor, table_name, condition: dict, what_extract="*", type_of_condition="LIKE"):
    """
    :rtype: list of dicts or dict in case of one row
    """
    """
    
    """
    query = f""" SELECT {what_extract} FROM {table_name} WHERE LOWER ("""
    for key in condition:
        query += f"""{key}) {type_of_condition} %({key})s OR LOWER ("""
    query = query.rstrip("OR LOWER (") + ";"
    cursor.execute(query, condition)
    result = cursor.fetchall()

    return result

@connection.connection_handler
def get_from_table_condition(cursor, table_name, condition: dict, what_extract="*"):
    """
    :rtype: list of dicts or dict in case of one row
    """
    query = f""" SELECT {what_extract} FROM {table_name} WHERE {next(iter(condition))} = %({next(iter(condition))})s;"""
    cursor.execute(query, condition)
    result = cursor.fetchall()

    return result
    # if len(result)>1:
    #     return result
    # else:
    #     # returns dict
    #     return next(iter(result))


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
    for key in data_to_update:
        update_query += f"""{key} = %({key})s, """
    update_query = update_query.rstrip(", ")

    update_query += f""" WHERE {next(iter(condition))} = %({next(iter(condition))})s;"""
    data_to_update.update(condition)

    cursor.execute(update_query, data_to_update)



@connection.connection_handler
def delete_data_in_table(cursor, table_name, condition):

    update_query = f"""DELETE FROM {table_name} """
    update_query += f"""WHERE {list(condition)[0]} = %({list(condition)[0]})s;"""

    cursor.execute(update_query, condition)


@connection.connection_handler
def insert_data_to_table(cursor, table_name, data_to_insert):

    insert_query = f"INSERT INTO {table_name} ("
    for key in data_to_insert:
        insert_query += f"{key}, "
    insert_query = insert_query.rstrip(', ') + ")"

    insert_query += f" VALUES ("
    for key in data_to_insert:
        insert_query += f"%({key})s, "
    insert_query = insert_query.rstrip(', ') + ")"

    cursor.execute(insert_query, data_to_insert)
