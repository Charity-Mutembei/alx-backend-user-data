#!/usr/bin/env python3

"""
Task 6: Basic Flask App
"""
from typing import Tuple
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, Response

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register():
    """
    email first
    """
    email = request.form.get('email')
    """
    followed by password
    """
    password = request.form.get('password')
    """
    check if user exists
    """
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    responds to post /sessions route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    """
    check boolean for response
    """
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    function to respond to the DELETE /sessions route.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    """
    If the user exists destroy the session and
    redirect the user to GET
    """
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        """
        If the user does not exist, respond with
        a 403 HTTP status.
        """
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    function to respond to the GET /profile route.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    """
    Use it to find the user. If the user exist,
    respond with a 200 HTTP status and the following
    JSON payload:
    """
    if user:
        return jsonify({"email": user.email}), 200
    else:
        """
        If the session ID is invalid or
        the user does not exist, respond with a
        403 HTTP status.
        """
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    function to respond to the POST /reset_password route.
    The request is expected to contain form data with
    the "email" field.
    """
    email = request.form.get('email')
    try:
        """
        generate a token and respond with a
        200 HTTP status and the following
        JSON payload:
        """
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        """
        If the email is not registered, respond with a
        403 status code
        """
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update a user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
