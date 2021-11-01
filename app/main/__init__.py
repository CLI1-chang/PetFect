"""
app.main __init__: main blueprint
Reference: O'Reilly Flask Web Development
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
