#!/usr/bin/env python3
"""
Module for managing user sessions.
"""

from models.base import Base


class UserSession(Base):
    """
    UserSession class to manage user sessions.
    This class inherits from Base and tracks user session information.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance """
        super().__init__(*args, **kwargs)  # Call the parent class constructor

        # Initialize user_id from keyword arguments
        self.user_id = kwargs.get('user_id')

        # Initialize session_id from keyword arguments
        self.session_id = kwargs.get('session_id')
