import pytest
from models.user_model import serialize_user

def test_serialize_user(sample_user):
    result = serialize_user(sample_user)
    expected = {
        "email": sample_user.get("email"),
        "name": sample_user.get("name", ""),
        "address": sample_user.get("address", ""),
        "role": sample_user.get("role", "cliente"),
    }
    assert result == expected