#!/usr/bin/env python3
"""
Task 4: Session cookie
"""
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """
    New class = Class Auth
    """

    def __int__(self):
        pass

    def require_auths(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Task 4: Session cookie
        """
        if path is None:
            return True
        elif path in excluded_paths:
            return False
        elif excluded_paths is None or excluded_paths == []:
            return True
        else:
            for i in excluded_paths:
                if path.startswith(i):
                    return False
                if i.startswith(path):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_headers(self, request=None) -> str:
        """
        Task 4
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_users(self, request=None) -> TypeVar('User'):
        """
        Task 4
        """
        return None

    def session_cookie(self, request=None):
        """
        Task 4
        """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
