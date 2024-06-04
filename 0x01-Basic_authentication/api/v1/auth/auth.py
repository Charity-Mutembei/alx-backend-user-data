#!/usr/bin/env python3
"""
Task 3: Auth Class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Task 3 Auth Class
    """

    def __int__(self):
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Decides whether a path needs authentication.
        Args:
            The path to be checked
            The paths that do not need to checked
        Return:
            Paths are true if not excluded, and false if excluded
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Nothing to return here
        Args:
            passed requests

        Returns:
            nothing
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Nothing to return
        Args:
           given requests
        Returns:
            nothing to return
        """
        return None
