#!/usr/bin/env python3
"""
Vew that handles all routes for the Session authentication.
"""
from typing import Tuple, Any
from os import getenv
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[Any, int]:
    """
    task 2
    """

    password = request.form.get('password')
    email = request.form.get('email')

    if not password:
        return jsonify({"error": "password missing"}), 400
    if not email:
        return jsonify({"error": "email missing"}), 400

    users = User.search({'email': email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.auth.session_auth import SessionAuth
            session_auth = SessionAuth()
            session_id = session_auth.create_session(user.id)
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            response = jsonify(user.to_json())
            return response
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> Tuple[Any, int]:
    """
    task 2
    """

    from api.v1.auth.session_auth import SessionAuth
    session_auth = SessionAuth()
    session_id = session_auth.destroy_session(request)
    if not session_id:
        abort(404)
    else:
        response.set_cookie(getenv('SESSION_NAME'), '')
        response = jsonify({}, 200)
    return response
