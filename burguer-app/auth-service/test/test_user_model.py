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

def test_serialize_incomplete_user():
    incomplete_user = {}
    result = serialize_user(incomplete_user)
    
    expected = {
        "email": None,
        "name": "",
        "address": "",
        "role": "cliente"
    }
    assert result == expected

def test_serialize_user_integer():
    # O with é usado para alertar que o próximo comando deve lançar um erro do tipo TypeError
    with pytest.raises(TypeError):
        serialize_user(123456789)

def test_serialize_user_string():
    # O with é usado para alertar que o próximo comando deve lançar um erro do tipo AttributeError
    with pytest.raises(AttributeError):
        serialize_user("not a user dict")


def test_serialize_unexpected_user():
    unexpected_user = {"unexpected_field": "unexpected_value"}
    result = serialize_user(unexpected_user)
    
    expected = {
        "email": None,
        "name": "",
        "address": "",
        "role": "cliente"
    }
    assert result == expected


def test_serialize_user_list():
    # quando uma lista é passada em vez de um dicionário
    with pytest.raises(AttributeError):
        serialize_user([{"email": "a@b.com"}])


def test_serialize_user_none():
    # quando None é passado como argumento
    with pytest.raises(AttributeError):
        serialize_user(None)


def test_serialize_user_null_values():
    # dicionário com valores nulos deve preservar os nulos
    null_user = {"email": None, "name": None, "address": None, "role": None}
    result = serialize_user(null_user)

    expected = {
        "email": None,
        "name": None,
        "address": None,
        "role": None,
    }
    assert result == expected

