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
                "name": "testuser",
                "address": "123 Main St",
                "role": "admin",
            },
            {
                "email": "test@example.com",
                "name": "testuser",
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
                "name": "",
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
                "name": "",
                "address": "",
                "role": "cliente",
            },
        ),
        (
            {"email": None, "name": None, "address": None, "role": None},
            {"email": None, "name": None, "address": None, "role": None},
        ),
        (
            {
                "email": 123,
                "name": ["list", "of", "names"],
                "address": {"street": "123 Main St"},
                "role": True,
            },
            {
                "email": 123,
                "name": ["list", "of", "names"],
                "address": {"street": "123 Main St"},
                "role": True,
            },
        ),
    ],
)
def test_serialize_user(input_user, expected_output):
    assert serialize_user(input_user) == expected_output


# Validate that invalid types raise AttributeError
@pytest.mark.parametrize(
    "invalid_input", ["this is not a dict", 12345, ["list", "of", "values"], None]
)
def test_serialize_user_invalid_type(invalid_input):
    with pytest.raises(AttributeError):
        serialize_user(invalid_input)
