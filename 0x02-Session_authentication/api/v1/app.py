#!/usr/bin/env python3
"""
Route module for the API.

This module initializes the Flask application, sets up the routes, and
handles authentication for the API. Different types of authentication
can be configured through environment variables.

Routes:
- /api/v1/status/
- /api/v1/unauthorized/
- /api/v1/forbidden/
- /api/v1/auth_session/login/
"""

from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views

def create_app():
    """Create and configure the Flask application.

    This function initializes the Flask application, registers the 
    app_views blueprint, and handles the configuration of the app.

    Returns:
        Flask: The initialized Flask application instance.
    """
    app = Flask(__name__)
    app.register_blueprint(app_views)
    # Enable Cross-Origin Resource Sharing (CORS) for the API
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    
    return app

# Initialize auth to None
auth = None

def load_auth():
    """Load the appropriate authentication class based on environment variable.

    This function checks the AUTH_TYPE environment variable and 
    initializes the corresponding authentication class.
    """
    global auth
    auth_type = getenv("AUTH_TYPE")
    if auth_type == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth_type == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()  # Create an instance of SessionAuth
    elif auth_type == "session_exp_auth":
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()  # Create an instance of SessionExpAuth
    elif auth_type == "session_db_auth":  # New condition for SessionDBAuth
        from api.v1.auth.session_db_auth import SessionDBAuth
        auth = SessionDBAuth()  # Create an instance of SessionDBAuth
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()

def before_request():
    """Method to handle actions before each request.

    This method checks if authentication is required for the incoming
    request and ensures that the user is authenticated. If not, it
    aborts the request with the appropriate status code.
    """
    if auth is None:
        return  # If auth is None, do nothing

    # List of paths that do not require authentication
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'  # Added new excluded path
    ]

    # Check if authentication is required for the current request path
    if not auth.require_auth(request.path, excluded_paths):
        return  # If the path does not require auth, do nothing

    # Check for authorization header and session cookie
    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)

    # Check if there is a current user
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)  # Raise 403 error if user is not authenticated

def register_hooks(app):
    """Register the before request hook and error handlers to the app.

    Args:
        app: The initialized Flask application instance.
    """
    app.before_request(before_request)

    @app.errorhandler(404)
    def not_found(error) -> str:
        """404 Not Found error handler.

        Returns a JSON response indicating that the requested resource was
        not found.

        Args:
            error: The error object containing information about the 404
                   error.

        Returns:
            A JSON response with a 404 status code.
        """
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(401)
    def unauthorized(error) -> str:
        """401 Unauthorized error handler.

        Returns a JSON response indicating that authentication is required
        and has failed.

        Args:
            error: The error object containing information about the 401
                   error.

        Returns:
            A JSON response with a 401 status code.
        """
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(error) -> str:
        """403 Forbidden error handler.

        Returns a JSON response indicating that the server understood the
        request, but it refuses to authorize it.

        Args:
            error: The error object containing information about the 403
                   error.

        Returns:
            A JSON response with a 403 status code.
        """
        return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    app = create_app()  # Create the Flask app
    load_auth()  # Load the appropriate authentication
    register_hooks(app)  # Register hooks to the app
    # Run the application on the specified host and port
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
