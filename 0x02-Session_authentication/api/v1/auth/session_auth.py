#!/usr/bin/env python3
"""
Module for managing session-based API authentication.

This module provides a class SessionAuth that handles session-related
authentication tasks, inheriting from the Auth class.
"""

from api.v1.auth.auth import Auth  # Import the Auth class
from flask import request
from typing import TypeVar
import uuid  # Import the uuid module to generate session IDs
from models.user import User  # Import the User model

UserType = TypeVar('User')


class SessionAuth(Auth):
    """
    Class to manage API authentication using sessions.
    This class inherits from Auth and currently implements session
    management functionality.
    """

    user_id_by_session_id = {}  # Class attr. to store user IDs by session ID

    def __init__(self):
        """ Initialize the SessionAuth class """
        super().__init__()  # Call the constructor of the parent class Auth

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a given user_id.

        Args:
            user_id (str): The user ID for which to create the session.

        Returns:
            str: The Session ID if successful, None otherwise.
        """
        if user_id is None:
            return None  # Return None if user_id is None
        if not isinstance(user_id, str):
            return None  # Return None if user_id is not a string

        # Generate a new Session ID
        session_id = str(uuid.uuid4())  # Generate a UUID for the session ID
        self.user_id_by_session_id[session_id] = user_id  # Store in dictionary

        return session_id  # Return the Session ID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve a User ID based on a given Session ID.

        Args:
            session_id (str): The Session ID for which to retrieve the User ID.

        Returns:
            str: The User ID if found, None otherwise.
        """
        if session_id is None:
            return None  # Return None if session_id is None
        if not isinstance(session_id, str):
            return None  # Return None if session_id is not a string

        # Use .get() to retrieve the User ID from the dictionary
        return self.user_id_by_session_id.get(session_id)  # Return the User ID

    def current_user(self, request=None) -> UserType:
        """
        Overloaded method to retrieve the current User instance based on
        session cookie.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            User: The User instance associated with the session cookie,
            or None if not found.
        """
        if request is None:
            return None  # Return None if request is None

        # Get the session cookie value
        session_id = self.session_cookie(request)

        # Retrieve the User ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None  # Return None if no User ID found

        # Retrieve the User instance from the database using the User ID
        # Assuming User.get(...) will fetch the User instance
        user = User.get(user_id)

        return user  # Return the User instance
