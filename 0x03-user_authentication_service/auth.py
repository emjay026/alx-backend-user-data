#!/usr/bin/env python3
"""
Auth module for password hashing.

This module provides functions for hashing passwords securely using bcrypt.
"""

import bcrypt
import uuid  # Import the uuid module
from db import DB
from user import User  # Ensure to import the User model
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

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

    def create_session(self, email: str) -> str:
        """Create a session for the user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID for the user.

        Raises:
            NoResultFound: If no user is found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)  # Find the user by email
        except NoResultFound:
            return None  # Handle the case where user does not exist

        session_id = _generate_uuid()  # Generate a new UUID for the session
        user.session_id = session_id  # Assign the session ID to the user
        self._db._session.commit()  # Save changes to the database
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve a user from the database using their session ID.

        Args:
            session_id (str): The session ID of the user.

        Returns:
            User or None: The User object if found, None otherwise.
        """
        if session_id is None:
            return None  # Return None if session_id is None

        try:
            # Attempt to find the user by session ID
            user = self._db.find_user_by(session_id=session_id)
            return user  # Return the user if found
        except NoResultFound:
            return None  # If no user is found, return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the user's session by updating the session ID to None.

        Args:
            user_id (int): The ID of the user whose session is to be destroyed.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)  # Find user by user_id
            user.session_id = None  # Set the session ID to None
            self._db._session.commit()  # Commit the changes to the database
        except NoResultFound:
            pass  # If no user is found, do nothing

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for the user associated with
        the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The generated reset token.

        Raises:
            ValueError: If a user with the given email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)  # Find the user by email
        except NoResultFound:
            # Raise ValueError if user does not exist
            raise ValueError(f"User with email {email} does not exist.")

        reset_token = _generate_uuid()  # Generate a new UUID for reset token
        user.reset_token = reset_token  # Update the user's reset_token field
        self._db._session.commit()  # Commit changes to the database

        return reset_token  # Return the generated reset token


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


def _generate_uuid() -> str:
    """Generate and return a new UUID as a string.

    Returns:
        str: A string representation of a new UUID.
    """
    return str(uuid.uuid4())
