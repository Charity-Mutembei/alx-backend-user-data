#!/usr/bin/env python3
"""
Task 0: 0. Et moi et moi et moi!
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from typing import Tuple, Any
import os
from flask_cors import (CORS, cross_origin)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth

    auth = SessionAuth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth

    auth = SessionDBAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth

    auth = SessionExpAuth()


@app.errorhandler(401)
def not_spotted(error) -> str:
    """ 401 handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def unauthorized_access(error) -> Tuple[Any, int]:
    """
        Not allowed to access resources
    Args:
        Error code

    Returns:
      A string for the message
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def bef_request():
    """
    request filter before handling the assigned route
    """
    if auth is None:
        pass
    else:
        setattr(request, "current_user", auth.current_user(request))
        excluded = [
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/',
            '/api/v1/status/',
            '/api/v1/unauthorized/',
        ]
        if auth.require_auth(request.path, excluded):
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")

            if auth.authorization_header(request) or \
                    auth.session_cookie(request) is None:
                abort(401, description="Unauthorized")


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
