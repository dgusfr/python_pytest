import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user_model import serialize_user


@pytest.mark.parametrize(
    "input_user, expected_output",
    [
        (
            {
                "email": "test@example.com",
                "username": "testuser",
                "address": "123 Main St",
                "role": "admin",
            },
            {
                "email": "test@example.com",
                "username": "testuser",
                "address": "123 Main St",
                "role": "admin",
            },
        ),
        (
            {
                "email": "teste@example.com",
            },
            {
                "email": "teste@example.com",
                "username": "",
                "address": "",
                "role": "cliente",
            },
        ),
        (
            # input
            {},
            # default output
            {
                "email": None,
                "username": "",
                "address": "",
                "role": "cliente",
            },
        ),
        (
            {"email": None, "username": None, "address": None, "role": None},
            {"email": None, "username": None, "address": None, "role": None},
        ),
        (
            {
                "email": 123,
                "username": ["list", "of", "names"],
                "address": {"street": "123 Main St"},
                "role": True,
            },
            {
                "email": 123,
                "username": ["list", "of", "names"],
                "address": {"street": "123 Main St"},
                "role": True,
            },
        ),
    ],
)
def test_serialize_user(input_user, expected_output):
    assert serialize_user(input_user) == expected_output
