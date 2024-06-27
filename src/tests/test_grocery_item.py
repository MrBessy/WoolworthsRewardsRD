# test/test_GroceryItem

import pytest
from src.modules import GroceryItem

@pytest.fixture
def sample_item():
    return GroceryItem("Apple", 1.99)

def test_initialization(sample_item):
    assert sample_item.get_item_name() == "Apple"
    assert sample_item.get_item_price() == 1.99

def test_getters(sample_item):
    assert sample_item.get_item_name() == "Apple"
    assert sample_item.get_item_price() == 1.99

def test_equality():
    item1 = GroceryItem("Apple", 1.99)
    item2 = GroceryItem("Apple", 1.99)
    item3 = GroceryItem("Orange", 0.99)

    assert item1 == item2  # Test equality of identical items
    assert item1 != item3  # Test inequality of different items

def test_equality_with_non_grocery_item():
    item = GroceryItem("Apple", 1.99)
    non_item = "Apple"

    assert item != non_item  # GroceryItem should not be equal to a non-GroceryItem object
