#!/usr/bin/env python3

"""
User model module for SQLAlchemy.
This module defines the User class representing the 'users' table
in the database.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the 'users' table.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The user's email address.
        hashed_password (str): The user's hashed password.
        session_id (str): The user's session ID, if any.
        reset_token (str): The user's password reset token, if any.
    """

    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """Return a string representation of the User instance."""
        return f"<User(id={self.id}, email={self.email})>"
