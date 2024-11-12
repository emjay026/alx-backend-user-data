#!/usr/bin/env python3
"""
Module for managing API authentication.

This module provides a class Auth to handle authentication-related tasks.
"""


from flask import request
from typing import List, TypeVar

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
        return False

    def authorization_header(self, request: request = None) -> str:
        """
        Get the authorization header from the request.

        Args:
            request (flask.Request, optional): The request object.
            Defaults to None.

        Returns:
            str: The authorization header, or None if not found.
        """
        return None

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
