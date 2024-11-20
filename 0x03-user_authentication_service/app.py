#!/usr/bin/env python3
"""
Flask application to manage user registration.

This application sets up an endpoint to register users through a JSON API.
"""

from flask import Flask, jsonify, request
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
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError as e:
        # If user already exists raise a ValueError
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
