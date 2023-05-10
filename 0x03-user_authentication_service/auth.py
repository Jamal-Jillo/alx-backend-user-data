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
