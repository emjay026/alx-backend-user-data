#!/usr/bin/env python3
"""
Module for managing database session authentication.

This module provides a class SessionDBAuth that inherits from
SessionExpAuth and handles session management using a database.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.user import User


class SessionDBAuth(SessionExpAuth):
    """
    Class to manage API authentication using sessions with database storage.
    This class inherits from SessionExpAuth and implements methods for
    session management.
    """

    def create_session(self, user_id=None) -> str:
        """ Create and store a new instance of UserSession. """
        # Call parent to create session ID
        session_id = super().create_session(user_id)

        if session_id is None:
            return None  # Return None if a Session ID can't be created

        # Create a new UserSession instance and save it to the database
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save the UserSession to the database

        return session_id  # Return the Session ID created

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Retrieve User ID based on session ID from the database. """
        if session_id is None:
            return None  # Return None if session_id is None

        # Retrieve UserSession instance based on session_id
        user_session = UserSession.get(session_id)

        if user_session is None:
            return None  # Return None if UserSession not found

        return user_session.user_id  # Return the user_id from UserSession

    def destroy_session(self, request=None) -> bool:
        """ Destroy the UserSession based on the Session ID from the request.
        """
        if request is None:
            return False  # Return False if request is None

        session_id = self.session_cookie(request)
        if session_id is None:  # If no session ID, return False
            return False

        # Retrieve UserSession instance to verify if it exists
        user_session = UserSession.get(session_id)

        if user_session is None:
            return False  # If UserSession not found, return False

        user_session.remove()  # Remove (destroy) the UserSession
        return True  # Return True indicating successful destruction of session
