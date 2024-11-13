#!/usr/bin/env python3
"""
Module for managing Basic Authentication.

This module provides the BasicAuth class, which extends
the Auth class to handle basic authentication methods.
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Class to manage basic authentication.

    Currently, this class is empty and serves as a placeholder for
    future implementation.
    """

    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """
        Extract the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
            authorization_header (str): The value of the Authorization header.

        Returns:
            str: The Base64 part of the Authorization header,
            or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]
