import pytest
from models.product_model import serialize_product

def test_serialize_product(sample_product):
    result = serialize_product(sample_product)
    expected = {
        "id": str(sample_product.get("_id")),
        "name": sample_product.get("name"),
        "description": sample_product.get("description"),
        "category": sample_product.get("category"),
        "price": sample_product.get("price"),
        "available": sample_product.get("available", True),
        "ingredients": sample_product.get("ingredients", [])
    }
    assert result == expected

def test_serialize_default_values():
    product_with_defaults = {
        "_id": "123",
        "name": "Test Product",
        "description": "A product for testing",
        "category": "Test Category",
        "price": 9.99
    }
    result = serialize_product(product_with_defaults)
    expected = {
        "id": "123",
        "name": "Test Product",
        "description": "A product for testing",
        "category": "Test Category",
        "price": 9.99,
        "available": True,
        "ingredients": []
    }
    assert result == expected

def test_serialize_product_convertion_id_to_string():
    product_with_object_id = {
        "_id": 123456789,
        "name": "Test Product",
        "description": "A product for testing",
        "category": "Test Category",
        "price": 9.99
    }
    result = serialize_product(product_with_object_id)
    expected = {
        "id": "123456789",
        "name": "Test Product",
        "description": "A product for testing",
        "category": "Test Category",
        "price": 9.99,
        "available": True,
        "ingredients": []
    }
    assert result == expected