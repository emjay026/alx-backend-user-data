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
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/') + '/'
        for excluded_path in excluded_paths:
            if path == excluded_path:
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
