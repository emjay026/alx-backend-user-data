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

User = TypeVar('User')


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
