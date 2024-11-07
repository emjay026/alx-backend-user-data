#!/usr/bin/env python3

"""
This module contains a function to obfuscate log messages
by redacting specified fields.
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates specified fields in a log message with a redaction string.

    Args:
        fields (list of str): A list of fields to obfuscate.
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
