from functools import wraps
from flask_login import current_user
from flask import jsonify


def role_required(role):
    # This is the decorator function that checks the user's role
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the user is authenticated and has the required role
            if current_user.is_authenticated:
                # Case 1: User has the exact required role
                if current_user.role == role:
                    return func(*args, **kwargs)  # Allow access to the protected route
                # Case 2: Admin has more power and can access all routes that regular users can
                elif role == "user" and current_user.role == "admin":
                    return func(*args, **kwargs)
                else:
                    return jsonify({"message": "You do not have the required permissions."}), 403
            else:
                return jsonify({"message": "You are not authenticated."}), 401  # Unauthorized

        return wrapper

    return decorator
