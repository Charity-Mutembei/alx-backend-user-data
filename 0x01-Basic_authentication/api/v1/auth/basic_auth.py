#!/usr/bin/env python3
"""
Task 6: basic auth class
"""
from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    """
    Task 6: basicAuth that takes in the Auth class
    """

    def __int__(self):
        pass

    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """
        Returns Authorization header-the Base64 part of the:
        Args:
            the Base64 part of the  authorization header:

        Returns:
            encoded values - A string of Base64
        """
        if authorization_header is None:
            return None

        if type(authorization_header) is not str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> str:
        """
        Task 8: Basic-Base64 decode
        Returns Base64 string-the decoded value of a
        Args:
            String to be decoded - base64_authorization_header

        Returns:
            Base64 string decoded value of a
        """
        import base64

        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            return base64.b64decode(base64_authorization_header) \
                .decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) \
            -> (str, str):

        """
        Returns the user email and password from the Base64 decoded value
        Args:
            decoded_base64_authorization_header: decoded string

        Returns:
            user email and password
        """
        if decoded_base64_authorization_header is None or \
                type(decoded_base64_authorization_header) is not str:
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) \
            -> TypeVar('User'):
        """
        Returns the User instance based on his email and password
        Args:
            user_email:
            user_pwd:

        Returns:

        """

        if user_email is None or type(user_email) is not str or \
                user_pwd is None or type(user_pwd) is not str:
            return None

        from models.user import User

        try:
            user = User.search({'email': user_email})
        except Exception:
            return None

        if user is None:
            return None
        else:
            for u in user:
                if u.is_valid_password(user_pwd):
                    return u
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves the User instance for a request
        Args:
            request:

        Returns:

        """
        authorization_header = self.authorization_header(request)
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)
        decoded_base64_authorization_header = \
            self.decode_base64_authorization_header(
                base64_authorization_header)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_authorization_header)
        return self.user_object_from_credentials(user_email, user_pwd)
