#!/usr/bin/env python3
"""
Flask application to manage user registration.

This application sets up an endpoint to register users through a JSON API.
"""

from flask import Flask, jsonify, request, abort, redirect
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
def logout() -> str:
    """Logout a user by destroying their session.

    Returns:
        jsonify: A JSON response indicating the result of the logout.
    """
    # Get session ID from cookies
    session_id = request.cookies.get("session_id")

    if session_id is None:
        # Handle the case where session ID is missing
        abort(403)

    # Find the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        # User does not exist, respond with 403
        abort(403)

    # User exists, destroy the session
    AUTH.destroy_session(user.id)

    # Respond with a success message and redirect to GET /
    return redirect("/")


@app.route('/profile', methods=['GET'])
def profile() -> jsonify:
    """Retrieve the user's profile information using the session ID.

    Returns:
        jsonify: A JSON response with the user's email if found,
                  or a 403 status if the session ID is invalid or
                  user does not exist.
    """
    # Get session ID from cookies
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)  # Handle case where session ID is missing

    # Find the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)  # User does not exist, respond with 403

    # Respond with the user's email and a 200 HTTP status
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> jsonify:
    """Generate a reset password token for a registered user.

    Returns:
        jsonify: A JSON response with the user's email and reset token,
                  or a 403 status if the email is not registered.
    """
    email: str = request.form.get('email') or ''

    # Check if the email is provided
    if not email:
        return jsonify({"message": "email field is required"}), 400

    try:
        # Generate a reset token through the AUTH object
        reset_token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        # If the email is not registered, respond with 403
        return jsonify({"message": "email not registered"}), 403


@app.route('/reset_password', methods=['PUT'])
def update_password() -> jsonify:
    """Update the user's password using the reset token.

    Returns:
        jsonify: A JSON response indicating the result of the password update,
                  with a 403 status for invalid tokens.
    """
    email: str = request.form.get('email') or ''
    reset_token: str = request.form.get('reset_token') or ''
    new_password: str = request.form.get('new_password') or ''

    # Check if all required fields are provided
    if not email or not reset_token or not new_password:
        return jsonify({
            "message": "email, reset_token, or new_password missing"
        }), 400

    try:
        # Update the password using the AUTH object
        AUTH.update_password(reset_token=reset_token, password=new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        # If the reset token is invalid, respond with 403
        return jsonify({"message": "Invalid reset token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
