import os
import sys
import pytest
import requests
import unittest.mock as mock
from unittest.mock import patch
from dotenv import load_dotenv

# Forçar uso de mongomock para testes
os.environ["USE_MOCK_DB"] = "1"

# Importar após definir variáveis de ambiente
from config.database import get_db


@pytest.fixture
def mongo_db():
    """Fixture que fornece instância de banco mockado para testes."""
    db = get_db()
    yield db
    # Limpar dados após cada teste
    db.drop_collection("users")
    db.drop_collection("orders")
    db.drop_collection("products")


@pytest.fixture
def base_url():
    return {
        "auth_service": "http://auth-service:8000/auth/",
        "user_service": "http://user-service:8001/user/",
        "order_service": "http://order-service:8002/order/",
    }


@pytest.fixture
def sample_user():
    return {
        "username": "testuser",
        "password": "TestPass123",
        "name": "Test User",
        "address": "123 Test St",
        "role": "customer",
    }


@pytest.fixture
def sample_itens():
    return {
        "item_name": "Test Burger",
        "item_description": "A delicious test burger",
    }


@pytest.fixture
def mock_user_service():
    with patch(requests.get) as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 302
        mock_response.headers = {"Location": "http://user-service:8001/user/testuser"}
        mock_response.json.return_value = {
            "username": "testuser",
            "name": "Test User",
            "address": "123 Test St",
            "role": "customer",
        }
    yield mock_get
