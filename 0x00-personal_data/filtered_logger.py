#!/usr/bin/env python3
"""
Write a function called filter_datum that
returns the log message obfuscated:
"""

import bcrypt
import csv
from typing import List
import logging
import re
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        function
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        function
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields, redaction, message, separator):
    """
    function
    """
    return re.sub(fr'(\b(?:{"|".join(fields)})=)[^;]*',
                  fr'\1{redaction}', message)


def get_logger() -> logging.Logger:
    """ Returns a logger object with RedactingFormatter """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


PII_FIELDS = ["name", "email", "phone", "ssn", "password"]


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to the database """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


def main():
    """
    Retrieves all rows in the users table and displays each
    row under a filtered format
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        logger.info("name={}; email={}; phone={}; ssn={};password={}; ip={}; last_login={}; user_agent={};".format(*row))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
