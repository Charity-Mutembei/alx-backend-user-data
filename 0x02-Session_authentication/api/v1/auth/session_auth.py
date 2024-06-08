#!/usr/bin/env python3
"""
Task 3
"""
from uuid import uuid4
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Task 3
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        task 3
        """
        if user_id is None:
            return None
        if user_id is not isinstance(user_id, str):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        task 3
        """
        if session_id is None:
            return None
        if session_id is not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        task 3
        """
        session_cookie = self.session_cookie(request)
        user = User.get(user_id)
        user_id = self.user_id_for_session_id(session_cookie)
        return user

    def destroy_session(self, request=None):
        """
        task 3
        """
        if request is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
