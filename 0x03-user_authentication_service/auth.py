#!/usr/bin/env python3
"""
Auth module for password hashing.

This module provides functions for hashing passwords securely using bcrypt.
"""

import bcrypt
from db import DB
from user import User  # Ensure to import the User model
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user in the database.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        # Check if user already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            # User does not exist, proceed with registration
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate the user's login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False


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
