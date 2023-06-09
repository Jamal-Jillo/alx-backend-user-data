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


def _generate_uuid() -> str:
    """Generates a UUID.
    """
    return str(uuid4())


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

    def valid_login(self, email, password):
        """Check if a user exists in the database and if the provided"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a new session ID for the user with the given email.

        Args:
            email (str): The email of the user to create a session for.

        Returns:
            str: The newly created session ID as a string.
            None: If no user was found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        user.session_id = session_id
        self._db.commit()

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a given session ID.
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user
