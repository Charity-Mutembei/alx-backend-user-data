#!/usr/bin/env python3
""" These are the index views models
"""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def statusview() -> str:
    """ The line command [GET /api/v1/status]
    Return:
      - the API status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def statsview() -> str:
    """ The line command [GET /api/v1/stats]
    Return:
      - the objects number
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorizedaccess() -> None:
    """ the line of command [GET /api/v1/unauthorized]
    Return:
      - the API status
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def unauthenticatedaccess() -> None:
    """the line of code is [GET /api/v1/forbidden]
    Return:
      - the API status
    """
    abort(403)
