#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import your view modules here
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Load User data after all routes are imported
User.load_from_file()

