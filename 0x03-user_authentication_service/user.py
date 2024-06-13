#!/usr/bin/env python3
"""
Task 0: User model
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model called User for database called
    users.
    """

    __tablename__ = "users"

    reset_token = Column(String(250), nullable=True)
    session_id = Column(String(250), nullable=True)
    hashed_password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
