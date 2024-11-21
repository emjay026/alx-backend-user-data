#!/usr/bin/env python3
"""A simple end-to-end (E2E) integration test for `app.py`.

This script tests various functionalities of the user management system,
including registration, login, profile access, logout, and password
reset functionalities.
"""

import requests

# Base URL for the application
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test the user registration functionality.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Asserts:
        - 200 status code when user registers successfully.
        - 400 status code when trying to register with an already
          registered email.
    """
    url = f"{BASE_URL}/users"
    body = {
        'email': email,
        'password': password,
    }

    # Register the user
    res = requests.post(url, data=body)
    print(res.status_code)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}

    # Attempt to register again with the same email
    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test logging in with an incorrect password.

    Args:
        email (str): The email of the user.
        password (str): The incorrect password of the user.

    Asserts:
        - 401 status code when trying to log in with wrong credentials.
    """
    url = f"{BASE_URL}/sessions"
    body = {
        'email': email,
        'password': password,
    }

    # Attempt to log in with wrong password
    res = requests.post(url, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test the login functionality and retrieve session ID.

    Args:
        email (str): The email of the user.
        password (str): The correct password of the user.

    Returns:
        str: The session ID if login is successful.

    Asserts:
        - 200 status code when login is successful.
    """
    url = f"{BASE_URL}/sessions"
    body = {
        'email': email,
        'password': password,
    }

    # Attempt to log in
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}

    # Return the session ID from cookies
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test retrieving profile information while logged out.

    Asserts:
        - 403 status code when access is denied due to being logged out.
    """
    url = f"{BASE_URL}/profile"

    # Attempt to access profile without being logged in
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test retrieving profile information while logged in.

    Args:
        session_id (str): The session ID of the logged-in user.

    Asserts:
        - 200 status code when access is granted.
        - User profile should include email information.
    """
    url = f"{BASE_URL}/profile"
    req_cookies = {
        'session_id': session_id,
    }

    # Access the profile using the session ID
    res = requests.get(url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Test logging out of a session.

    Args:
        session_id (str): The session ID of the user to log out.

    Asserts:
        - 200 status code when logout is successful.
    """
    url = f"{BASE_URL}/sessions"
    req_cookies = {
        'session_id': session_id,
    }

    # Log out the user
    res = requests.delete(url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test requesting a password reset token.

    Args:
        email (str): The email of the user requesting a reset.

    Returns:
        str: The reset token if the request is successful.

    Asserts:
        - 200 status code when the reset token is successfully issued.
    """
    url = f"{BASE_URL}/reset_password"
    body = {
        'email': email,
    }

    # Request a password reset token
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()

    # Return the reset token
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating a user's password using a reset token.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset token obtained from a password reset
                           request.
        new_password (str): The new password to set for the user.

    Asserts:
        - 200 status code when the password is updated successfully.
    """
    url = f"{BASE_URL}/reset_password"
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }

    # Update the user's password
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


# Constants for testing
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    # Run the integration tests sequentially
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
