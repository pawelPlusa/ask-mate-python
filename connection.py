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

    if user_name and password and host and database_name:

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
        connection = psycopg2.connect(get_connection_string())
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
        dict_cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return_value = function(dict_cursor, *args, **kwargs)
        dict_cursor.close()
        connection.close()
        return return_value

    return wrapper
