#!/usr/bin/env python3
"""
Route module for the API.
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(app_views)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    return app

def load_auth():
    """Load the appropriate authentication class based on environment variable.
    """
    auth_type = getenv("AUTH_TYPE")
    auth = None  # Initialize auth without global scope
    
    if auth_type == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth_type == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif auth_type == "session_exp_auth":
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    elif auth_type == "session_db_auth":
        from api.v1.auth.session_db_auth import SessionDBAuth
        auth = SessionDBAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()

    return auth

app = create_app()  # Create the Flask app
auth = load_auth()  # Load the appropriate authentication

@app.before_request
def before_request():
    """Before request handler for authentication."""
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """404 Not Found error handler."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error):
    """401 Unauthorized error handler."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """403 Forbidden error handler."""
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
