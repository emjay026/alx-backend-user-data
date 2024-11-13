#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth to None
auth = None

# Load authentication type from environment variable
auth_type = getenv("AUTH_TYPE")
if auth_type == "basic_auth":
    from auth.v1.auth.auth import BasicAuth
    auth = BasicAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request():
    """Method to handle before request actions."""
    if auth is None:
        return  # If auth is None, do nothing

    # List of paths that do not require authentication
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    # Check if authentication is required for the current request path
    if not auth.require_auth(request.path, excluded_paths):
        return  # If the path does not require auth, do nothing

    # Check for authorization header
    if auth.authorization_header(request) is None:
        abort(401)  # Raise 401 error if no authorization header is present

    # Check if there is a current user
    if auth.current_user(request) is None:
        abort(403)  # Raise 403 error if user is not authenticated


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
