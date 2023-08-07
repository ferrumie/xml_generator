import logging
from sqlite3 import Connection, connect, Error
from _typeshed import StrOrBytesPath

def create_connection(db_file: StrOrBytesPath) -> Connection | None:
    conn = None
    try:
        conn = connect(db_file)
    except Error as e:
        logging.error('Database connection error: %s', e)

    return conn