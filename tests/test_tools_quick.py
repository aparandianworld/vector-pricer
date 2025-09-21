from src.chatbot.tools import get_product_price, get_product_features  # Fixed import name
from config.settings import settings
import pytest

def test_get_product_price():
    """Test price lookup for existing product."""
    result = get_product_price("MacBook Air")
    assert "1499.99" in result
    assert "The price of MacBook Air" in result

def test_get_product_price_missing():
    """Test price lookup for non-existent product."""
    result = get_product_price("Fake Product")
    assert "Price not found" in result

def test_get_product_features():
    """Test features lookup for existing product."""
    result = get_product_features("MacBook Pro")
    assert "M1 chip" in result
    assert "16GB RAM" in result

def test_get_product_features_missing():
    """Test features lookup for non-existent product."""
    result = get_product_features("Fake Product")
    assert "Features not found" in result

if __name__ == "__main__":
    print("=== Manual Tool Testing ===")
    print("1. Price test:", get_product_price("MacBook Air"))
    print("2. Features test:", get_product_features("MacBook Pro"))
    print("3. Missing price (invalid product):", get_product_price("Fake Product"))
    print("4. Missing features (invalid product):", get_product_features("Fake Product"))