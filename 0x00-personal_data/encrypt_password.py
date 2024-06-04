#!/usr/bin/env python3
"""
User passwords should NEVER be stored in plain text in a database.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Returns a salted, hashed password as a byte string """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Returns True if the provided password matches
    the hashed password, else False
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))
