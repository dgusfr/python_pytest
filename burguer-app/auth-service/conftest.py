import os
import sys
import pytest
import requests
import unittest.mock as mock, patch
from pymongo import MongoClient
from dotenv import load_dotenv


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
    with patch(requests.get) as mock_requests:
        yield mock_requests
