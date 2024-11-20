#!/usr/bin/env python3
"""
Flask application to manage user registration.

This application sets up an endpoint to register users through a JSON API.
"""

from flask import Flask, jsonify, request, abort
from auth import Auth

# Initialize a Flask application
app = Flask(__name__)

# Instantiate the Auth object
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> jsonify:
    """Return a welcome message in JSON format.

    Returns:
        jsonify: A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> jsonify:
    """Register a new user with email and password.

    Returns:
        jsonify: A JSON response indicating the result of the registration.
    """
    # Expect 'email' and 'password' in form data
    email: str = request.form.get('email') or ''
    password: str = request.form.get('password') or ''

    # Check if both fields are provided
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        # Register the user through the AUTH object
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> jsonify:
    """Login a user and create a session.

    Returns:
        jsonify: A JSON response indicating the result of the login.
    """
    email: str = request.form.get('email') or ''
    password: str = request.form.get('password') or ''

    # Verify that both fields are provided
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    # Validate login credentials
    if not AUTH.valid_login(email=email, password=password):
        abort(401)  # Respond with a 401 HTTP status for unauthenticated access

    # Create a new session for the user if login is successful
    session_id = AUTH.create_session(email)

    # Set the session ID in a cookie
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> jsonify:
    """Logout a user by destroying their session.

    Returns:
        jsonify: A JSON response indicating the result of the logout.
    """
    # Get session ID from cookies
    session_id = request.cookies.get("session_id")

    if session_id is None:
        # Handle the case where session ID is missing
        return '', 403

    # Find the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        # User does not exist, respond with 403
        return '', 403

    # User exists, destroy the session
    AUTH.destroy_session(user.id)

    # Respond with a success message and redirect to GET /
    return jsonify({"message": "logged out"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
