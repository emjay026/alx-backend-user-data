#!/usr/bin/env python3
"""
Module for managing session expiration authentication.

This module provides a class SessionExpAuth that inherits from
SessionAuth and handles session management with expiration timing.
"""

from api.v1.auth.session_auth import SessionAuth  # Import SessionAuth class
from datetime import datetime, timedelta  # Import datetime and timedelta
import os  # To access environment variables


class SessionExpAuth(SessionAuth):
    """
    Class to manage API authentication using sessions with expiration.
    This class inherits from SessionAuth and implements session expiration
    functionality.
    """

    def __init__(self):
        """ Initialize the SessionExpAuth class """
        super().__init__()  # Call the constructor of parent class SessionAuth

        # Get SESSION_DURATION and cast to an integer, default to 0 if invalid
        session_duration = os.getenv("SESSION_DURATION")
        try:
            self.session_duration =\
                int(session_duration) if session_duration else 0
        except ValueError:
            self.session_duration = 0  # Assign 0 if parsing fails

    def create_session(self, user_id=None):
        """ Create a Session ID for a user ID with session expiration. """
        session_id = super().create_session(user_id)  # Call the parent method

        if session_id is None:
            return None  # Return None if a Session ID can't be created

        # Create a session dictionary to store additional session info
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()  # Store the current datetime
        }

        return session_id  # Return the Session ID created

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve User ID based on session ID with expiration logic. """
        if session_id is None:
            return None

        # Check if the session_id exists in the dictionary
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None  # Return None if session ID not found

        # Check expiration logic
        if self.session_duration <= 0:
            return session_data["user_id"]

        created_at = session_data.get("created_at")
        if created_at is None:
            return None  # Return None if no creation time was found

        # Calculate expiration time
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None  # Session has expired

        return session_data["user_id"]  # Return the user ID if still valid
