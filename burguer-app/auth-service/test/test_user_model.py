import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user_model import serialize_user


def test_complete_user():
    user_test = {
        "email": "testuser@example.com",
        "name": "",
        "address": "",
        "role": "cliente",
    }

    result = serialize_user(user_test)

    expected = {
        "email": "testuser@example.com",
        "name": "",
        "address": "",
        "role": "cliente",
    }

    assert result == expected


def test_user_string():
    with pytest.raises(AttributeError):
        serialize_user("this is not a dict")


def test_user_empty_dict():
    user_test = {}

    result = serialize_user(user_test)

    expected = {
        "email": None,
        "name": "",
        "address": "",
        "role": "cliente",
    }

    assert result == expected


def test_user_missing_email():
    user_test = {"name": "John Doe"}

    result = serialize_user(user_test)

    expected = {
        "email": None,
        "name": "John Doe",
        "address": "",
        "role": "cliente",
    }

    assert result == expected


def test_security_password_filter():
    # 1. Entrada com um dado sensível (password)
    user_input = {
        "email": "admin@teste.com",
        "password": "minha_senha_secreta",
        "role": "admin",
    }

    result = serialize_user(user_input)

    expected = {
        "email": "admin@teste.com",
        "password": "minha_senha_secreta",  # Passa a senha mas ela não existe no serializer
        "name": "",
        "address": "",
        "role": "admin",
    }

    # Vai falhar aqui
    assert result == expected


def test_user_dict_none():
    with pytest.raises(AttributeError):
        serialize_user(None)
