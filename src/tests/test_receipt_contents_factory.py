# test/test_ReceiptContentsFactory

import pytest
from src.modules import ReceiptContentsFactory
from src.modules import DigitalReceipt
from src.modules import GroceryItem

# Mock data for testing
@pytest.fixture
def sample_item_dict():
    return {
        "Item1": 10.0,
        "Item2": 15.0,
        "Item3": 5.0
    }

@pytest.fixture
def sample_total():
    return 30.0

@pytest.fixture
def sample_EDR_discount_bool():
    return True

# Test case for ReceiptContentsFactory class
def test_create_grocery_items(sample_item_dict):
    factory = ReceiptContentsFactory()
    grocery_items = factory._create_grocery_items(sample_item_dict)

    assert isinstance(grocery_items, dict)
    assert len(grocery_items) == len(sample_item_dict)

    for item_name, grocery_item_obj in grocery_items.items():
        assert isinstance(grocery_item_obj, GroceryItem)
        assert grocery_item_obj.get_item_name() == item_name
        assert grocery_item_obj.get_item_price() == sample_item_dict[item_name]

def test_create_digital_receipt(sample_item_dict, sample_total, sample_EDR_discount_bool):
    factory = ReceiptContentsFactory()
    receipt = factory.create_digital_recipet(sample_item_dict, sample_total, sample_EDR_discount_bool)

    assert isinstance(receipt, DigitalReceipt)
    assert receipt.get_receipt_total() == sample_total * receipt.get_everyday_extra_discount()
    assert receipt.get_everyday_extra_discount() == 0.9

    for item_name, item_price in receipt.get_receipt_items().items():
        assert item_name in receipt.get_receipt_items()
        assert receipt.get_receipt_items()[item_name] == item_price