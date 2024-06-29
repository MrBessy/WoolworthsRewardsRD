# test/test_GroceryItem

import pytest
from src.main.dependencies.modules import GroceryItem

@pytest.fixture
def sample_item():
    item = GroceryItem()
    item.set_item_name("Apple")
    item.set_item_price(1.99)
    return item

def test_initialization(sample_item):
    assert sample_item.get_item_name() == "Apple"
    assert sample_item.get_item_price() == 1.99

def test_getters(sample_item):
    assert sample_item.get_item_name() == "Apple"
    assert sample_item.get_item_price() == 1.99

def test_equality(sample_item):
    item1 = sample_item
    item2 = sample_item

    item3 = GroceryItem()
    item3.set_item_name("Orange")
    item3.set_item_price(0.99)

    assert item1 == item2  # Test equality of identical items
    assert item1 != item3  # Test inequality of different items

def test_equality_with_non_grocery_item(sample_item):
    non_item = "Apple"

    assert sample_item != non_item  # GroceryItem should not be equal to a non-GroceryItem object
