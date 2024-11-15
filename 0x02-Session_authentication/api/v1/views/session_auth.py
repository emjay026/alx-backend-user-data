#!/usr/bin/env python3
"""
Module for handling session authentication routes.
"""

from flask import jsonify, request, abort
from models.user import User  # Import the User model
import os  # To access environment variables
from api.v1.views import app_views  # Import the blueprint
from api.v1.app import auth  # Import the auth for session management


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /api/v1/auth_session/login
    Handle user login for session authentication.

    Returns:
        JSON response with user information and session cookie if
        successful.
    """

    email = request.form.get('email')  # Retrieve the email from form data
    password = request.form.get('password')  # Retrieve the password

    if not email:  # Check if email is missing or empty
        return jsonify({"error": "email missing"}), 400

    if not password:  # Check if password is missing or empty
        return jsonify({"error": "password missing"}), 400

    # Search for the User instance based on the email
    user_list = User.search({"email": email})

    # Check if a user was found
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_list[0]  # Get the first user from the list (if any)

    # Check if the password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401  # Wrong password

    # Create the session ID for the user
    session_id = auth.create_session(user.id)  # Assuming user.id is the ID

    # Prepare the response with user details
    response = jsonify(user.to_json())  # Get user JSON representation
    session_name = os.getenv("SESSION_NAME")  # Get the cookie name

    # Set the session ID as a cookie in the response
    response.set_cookie(session_name, session_id)  # Set the cookie

    return response  # Return response with user details and cookie


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    DELETE /api/v1/auth_session/logout
    Handle user logout by destroying the session.

    Returns:
        Empty JSON response if the logout was successful.
    """
    # Use the auth object to destroy the session
    if not auth.destroy_session(request):
        abort(404)  # If destroy_session returns False, abort with 404

    # Return an empty JSON dictionary with status code 200
    return jsonify({}), 200
