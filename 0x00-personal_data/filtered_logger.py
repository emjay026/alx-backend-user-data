#!/usr/bin/env python3

"""
This module contains functions to obfuscate log messages by redacting
specified fields and a logging formatter for redaction.
"""

import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message with a redaction string.

    Args:
        fields (List[str]): A list of fields to obfuscate.
        redaction (str): The string to replace the fields with.
        message (str): The log message that contains the fields.
        separator (str): The character that separates fields in log message.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    return re.sub(
        f'({"|".join(map(re.escape, fields))})=[^;]*',
        lambda m: f"{m.group(0).split('=')[0]}={redaction}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with redacted fields."""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, ";")
        return super().format(record)


# Constant for PII fields
PII_FIELDS: tuple = ("email", "ssn", "password", "phone", "last_login")


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
