#!/usr/bin/env python3

"""
Task 9
"""
from datetime import time
from api.v1.auth.auth import Auth
from os import getenv


class SessionExpAuth(Auth):
    """
    Task 9
    """

    def __init__(self):
        """
        Task 9 Initialize SessionExpAuth
        """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
        task 9
        """
        id = super().create_session(user_id)
        if id is None:
            return None
        self.user_id_by_session_id[id] = {"user_id": user_id, "created_at": time.time()}
        if user_id is None or not isinstance(user_id, str):
            return None
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Task 9
        """
        session = self.user_id_by_session_id.get(session_id)
        if session is None:
            return None
        if session_id is None or not isinstance(session_id, str):
            return None
        if time.time() - session.get("created_at") > self.session_duration:
            return None
        if self.session_duration <= 0:
            return session.get("user_id")
        return session.get("user_id")
