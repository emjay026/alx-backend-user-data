#!/usr/bin/env python3
"""
Module for password encryption functions.

This module provides functions to hash passwords securely using the
bcrypt library and to validate provided passwords against hashed
passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password with bcrypt and return the salted hash as a byte string.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: A byte string representing the salted hash of the password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to validate.

    Returns:
        bool: True if the password matches the hashed password,
              False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
