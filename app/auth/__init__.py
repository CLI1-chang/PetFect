"""
app.auth __init__: auth blueprint
Reference: O'Reilly Flask Web Development
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
