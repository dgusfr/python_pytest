import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user_model import serialize_user


def test_serialize_user():
    user_test = {"id": 1, "username": "testuser", "email": "testuser@example.com"}
    result = serialize_user(user_test)
    expected = {"id": 1, "username": "testuser", "email": "testuser@example.com"}

    assert result == expected
