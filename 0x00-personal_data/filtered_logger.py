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


def main():
    """Main function to retrieve and display user data in filtered format."""
    db_connection = get_db()

    if db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users;")  # Query to retrieve all users
        rows = cursor.fetchall()

        # Define the filtered fields that need to be redacted
        filtered_fields = ['name', 'email', 'phone', 'ssn', 'password']
        redaction_format = "[HOLBERTON] user_data INFO {}: {};"

        # Iterate through each row
        for row in rows:
            # Assuming row structure has the necessary columns:
            # This is a placeholder for all user data; adapt as necessary
            user_data = {
                'name': row[0],  # Assuming these correspond to correct index
                'email': row[1],
                'phone': row[2],
                'ssn': row[3],
                'password': row[4],
                'ip': row[5],
                'last_login': row[6],
                'user_agent': row[7],
            }

            # Format the time for demo purposes (replace with actual timestamp)
            timestamp = "2023-10-01 10:10:10,000"  # Placeholder timestamp.

            # Prepare message for redaction
            message = "; ".join(
                f"{key}={user_data[key]}" for key in user_data.keys()
            )

            # Redact sensitive data
            redacted_message = filter_datum(
                filtered_fields, "***", message, ";")

            # Print final formatted message
            print(redaction_format.format(timestamp, redacted_message))

        cursor.close()
        db_connection.close()


if __name__ == "__main__":
    main()
