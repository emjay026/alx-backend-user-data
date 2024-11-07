#!/usr/bin/env python3

"""
This module contains functions to obfuscate log messages by redacting
specified fields and a logging formatter for redaction.
"""

import logging
import re
import os
import mysql.connector
from typing import List
from mysql.connector import Error

# Constant for PII fields
PII_FIELDS: tuple = ("name", "email", "ssn", "password", "phone")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates specified fields in log message with a redaction string."""
    return re.sub(
        rf'({"|".join(map(re.escape, fields))})=[^ {separator}]*',
        lambda m: f"{m.group(0).split('=')[0]}={redaction}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with redacted fields."""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for user data.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db():
    """Function that returns a connector to the database."""

    # Retrieve environment variables, with defaults
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    # Check if the database name is set
    if not database:
        raise ValueError(
            "The environment variable PERSONAL_DATA_DB_NAME is not set.")

    try:
        # Create a connection to the database
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )

        if connection.is_connected():
            return connection

    except Error as e:
        return None
