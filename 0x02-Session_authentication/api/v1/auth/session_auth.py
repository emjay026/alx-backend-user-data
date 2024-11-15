#!/usr/bin/env python3
"""
Module for managing session-based API authentication.

This module provides a class SessionAuth that handles session-related
authentication tasks, inheriting from the Auth class.
"""

from api.v1.auth.auth import Auth
from flask import request
from typing import TypeVar

User = TypeVar('User')


class SessionAuth(Auth):
    """
    Class to manage API authentication using sessions.
    This class inherits from Auth and currently does not implement any
    additional functionality.
    """

    def __init__(self):
        """ Initialize the SessionAuth class """
        super().__init__()  # Call the constructor of the parent class Auth
