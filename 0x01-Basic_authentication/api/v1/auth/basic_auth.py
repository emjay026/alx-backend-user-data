#!/usr/bin/env python3
"""
Module for managing Basic Authentication.

This module provides the BasicAuth class, which extends
the Auth class to handle basic authentication methods.
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Tuple

UserType = TypeVar('User')


class BasicAuth(Auth):
    """
    Class to manage basic authentication.

    Currently, this class is empty and serves as a placeholder for
    future implementation.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
            authorization_header (str): The value of the Authorization
            header.

        Returns:
            str: The Base64 part of the Authorization header, or None if
            invalid.
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
            -> Tuple[str, str]:
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

        # Split the decoded string into email and password on the first colon
        if ":" not in decoded_base64_authorization_header:
            return None, None

        # This will split on the first occurrence of colon
        user_email, user_pwd =\
            decoded_base64_authorization_header.split(":", 1)

        return user_email, user_pwd

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> UserType:
        """
        Get the User instance based on the user email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance or None if invalid credentials.
        """
        # Check for valid email and password
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Use the User class's search method to find a user by email
        users = User.search({"email": user_email})

        # Check if any user was found
        if len(users) == 0:
            return None  # No user found

        user = users[0]  # Assume email is unique, get the first match

        # Validate password
        if not user.is_valid_password(user_pwd):
            return None  # Invalid password

        return user  # Return the User instance found

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current User instance from a request.

        Args:
            request: The HTTP request object.

        Returns:
            User: The User instance if found, or None if invalid.
        """
        if request is None:
            return None

        # Get the authorization header
        auth_header = self.authorization_header(request)

        # Extract the Base64 part from the header
        base64_auth_header =\
            self.extract_base64_authorization_header(auth_header)

        # Decode the Base64 authorization header
        decoded_auth_header =\
            self.decode_base64_authorization_header(base64_auth_header)

        # Extract email and password from the decoded string
        user_email, user_pwd =\
            self.extract_user_credentials(decoded_auth_header)

        # Retrieve the User object based on email and password
        return self.user_object_from_credentials(user_email, user_pwd)
