"""
Creates a decorator to handle the database connection/cursor opening/closing.
Creates the cursor with RealDictCursor, thus it returns real dictionaries, where the column names are the keys.
"""

import os
import psycopg2
import psycopg2.extras


def get_connection_string():
    """
    setup connection string
    to do this, please define these environment variables first
    """

    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    print(user_name, password, host, database_name)

    if env_variables_defined:

        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError(f'Some necessary environment variable(s) are not defined')


def open_database():
    """
    Establish new database connection based on data received form get_connection_string
    """

    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True

    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception

    return connection


def connection_handler(function):
    """
    Connection handler decorator
    """

    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper


"""this part refers to old csv functionality"""

# TODO: Remove what bellove after full conversion to SQL:
import csv


def open_file(filename: str) -> list:
    """
    simpler variation of open_file function
    """
    with open(filename, newline='') as csvfile:
        return [(dict(row)) for row in csv.DictReader(csvfile)]


def save_file(data_to_write: list, filename: str):
    fieldnames = list(data_to_write[0].keys())
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in data_to_write:
            writer.writerow(line)
