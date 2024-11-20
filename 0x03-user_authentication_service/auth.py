#!/usr/bin/env python3
"""
Auth module for password hashing.

This module provides functions for hashing passwords securely using bcrypt.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with a generated salt.

    Args:
        password (str): The plain password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password
