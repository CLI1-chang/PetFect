"""
app.decorators: decorators for roles
Reference: O'Reilly Flask Web Development
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import User


def permission_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_administrator():
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required()(f)
