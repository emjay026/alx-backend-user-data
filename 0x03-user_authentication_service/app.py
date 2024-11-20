#!/usr/bin/env python3
"""
Flask application to return a welcome message.

This application sets up a single route that returns a JSON message.
"""

from flask import Flask, jsonify

# Initialize a Flask application
app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    """Return a welcome message in JSON format."""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
