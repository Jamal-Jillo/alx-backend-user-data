#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """"""
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt and return the result
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth object."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user in the authentication database.

        Args:
            email (str): Email of the new user.
            password (str): Password of the new user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user already exists with the given email.
        """

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        pwd_hash = _hash_password(password)
        user = self._db.add_user(email, pwd_hash)
        return user
