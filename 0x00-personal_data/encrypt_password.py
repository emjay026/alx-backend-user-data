#!/usr/bin/env python3
"""
Module for password encryption functions.

This module provides functions to hash passwords securely
using the bcrypt library.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password with bcrypt and return salted hash as a byte string.

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
