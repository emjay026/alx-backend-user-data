#!/usr/bin/env python3
"""
Module for managing Basic Authentication.

This module provides the BasicAuth class, which extends
the Auth class to handle basic authentication methods.
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Class to manage basic authentication.

    Currently, this class is empty and serves as a placeholder for
    future implementation.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str)\
            -> str:
        """
        Extract the Base64 part of the Authorization header for
        Basic Authentication.

        Args:
            authorization_header (str): The value of the
            Authorization header.

        Returns:
            str: The Base64 part of the Authorization header, or
            None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """
        Decode the Base64 string and return the decoded value.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded value as UTF-8 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (ValueError, TypeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):
        """
        Extract the user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str): The decoded
            Base64 string.

        Returns:
            tuple: A tuple containing the user email and the user password,
                   or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None

        # Split the decoded string into email and password
        return decoded_base64_authorization_header.split(":", 1)
