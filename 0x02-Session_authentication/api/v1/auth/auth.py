#!/usr/bin/env python3
"""
Module for managing API authentication.

This module provides a class Auth to handle authentication-related tasks.
"""

from flask import request
from typing import List, TypeVar
import os  # Import os module for accessing environment variables

User = TypeVar('User')


class Auth:
    """
    Class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): The list of excluded paths.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the path for trailing slashes
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            # Handle wildcard paths that end with *
            if excluded_path.endswith('*'):
                # Remove the '*' and normalize the excluded path
                normalized_excluded_path = excluded_path[:-1].rstrip('/') + '/'
                if path.startswith(normalized_excluded_path):
                    return False
            else:
                # Normalize the excluded path
                normalized_excluded_path = excluded_path.rstrip('/') + '/'
                if path == normalized_excluded_path:
                    return False

        return True

    def authorization_header(self, request: request = None) -> str:
        """
        Get the authorization header from the request.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            str: The authorization header, or None if not found.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request: request = None) -> User:
        """
        Get the current user from the request.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            User: The current user, or None if not found.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Retrieve the session cookie value from the request.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            str: The session cookie value if found, None otherwise.
        """
        if request is None:
            return None  # Return None if request is None

        # Get cookie name from the environment variable
        session_name = os.getenv("SESSION_NAME")
        # Return the value of the cookie named _my_session_id
        return request.cookies.get(session_name)
