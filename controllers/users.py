from flask import Blueprint, request, jsonify

from connector.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from models.users import User
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select
import re

users_blueprints = Blueprint("users_blueprints", __name__)


@users_blueprints.route("/register", methods=["POST"])
def register():
    # Create a new session for database operations
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        s.begin()
        data = request.form.to_dict()

        required_fields = ["name", "email", "password"]
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"message": f"Oops! The '{field}' field is missing. Please fill it in and try again."}),
                    400,
                )
            if not data[field]:
                return (
                    jsonify(
                        {
                            "message": f"Oops! It looks like you didn't enter a value for '{field}'. Please complete the form."
                        }
                    ),
                    400,
                )

        if not re.match(email_regex, data["email"]):
            return (
                jsonify({"message": "Hmm, that doesn’t look like a valid email address. Please check and try again."}),
                400,
            )

        existing_user = s.query(User).filter((User.name == data["name"]) | (User.email == data["email"])).first()

        if existing_user:
            return (
                jsonify(
                    {"message": "It seems like the name or email is already in use. Please choose a different one."}
                ),
                400,
            )

        # Create a new user and set the password
        new_user = User(name=data["name"], email=data["email"])
        new_user.set_password(data["password"])

        # Add the new user to the session and commit the transaction
        s.add(new_user)
        s.commit()

    except Exception as e:
        # Rollback the session if an error occurs
        s.rollback()
        return (
            jsonify(
                {
                    "message": f"Something went wrong while processing your registration. Please try again later. Error details: {str(e)}"
                }
            ),
            500,
        )

    finally:
        # Close the session
        s.close()

    # If everything is successful, return a success message
    return jsonify({"message": "Congratulations! You have successfully registered. Welcome aboard!"}), 200


@users_blueprints.route("/login", methods=["POST"])
def login():
    # Create a new session for database operations
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        s.begin()
        data = request.form.to_dict()

        required_fields = ["email", "password"]
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"message": f"Oops! The '{field}' field is missing. Please fill it in and try again."}),
                    400,
                )
            if not data[field]:
                return (
                    jsonify(
                        {
                            "message": f"Oops! It looks like you didn't enter a value for '{field}'. Please complete the form."
                        }
                    ),
                    400,
                )

        if not re.match(email_regex, data["email"]):
            return (
                jsonify({"message": "Hmm, that doesn’t look like a valid email address. Please check and try again."}),
                400,
            )

        user = s.query(User).filter(User.email == data["email"]).first()

        if user is None:
            return (
                jsonify({"message": "Hmm, we couldn't find an account with that email. Please check and try again."}),
                403,
            )

        if not user.check_password(data["password"]):
            return jsonify({"message": "Oops! The password you entered is incorrect. Please try again."}), 403

        login_user(user)

        session_id = request.cookies.get("session")

        return jsonify({"session_id": session_id, "message": "Welcome back! You've successfully logged in."}), 200

    except Exception as e:
        s.rollback()
        return (
            jsonify(
                {"message": f"Something went wrong while logging in. Please try again later. Error details: {str(e)}"}
            ),
            500,
        )

    finally:
        s.close()


@users_blueprints.route("/user", methods=["GET"])
@login_required
def profile():
    # Create a new session for database operations
    Session = sessionmaker(bind=connection)
    s = Session()

    try:
        # Begin the transaction
        s.begin()

        # Query all users from the database
        users = s.query(User).all()

        # If no users found, return a message
        if not users:
            return jsonify({"message": "No users found in the database."}), 404

        # Prepare the user data to be displayed
        all_users = []
        for user in users:
            user_info = {
                "name": user.name,
                "email": user.email,
                # Add any other fields you want to include in the user profile
            }
            all_users.append(user_info)

        # Return the list of all users
        return jsonify({"message": "Users retrieved successfully.", "users": all_users}), 200

    except Exception as e:
        # Handle any exceptions that may occur
        s.rollback()
        return jsonify({"message": f"Failed to retrieve users. Error details: {str(e)}"}), 500

    finally:
        # Close the session
        s.close()


@users_blueprints.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return {"message": "Success logout"}
