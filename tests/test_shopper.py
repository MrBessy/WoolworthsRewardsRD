import pytest
from src.main.dependencies.modules import GroceryItem, Shopper

@pytest.fixture
def sample_shopper():
    shopper = Shopper()
    shopper.set_name("John Doe")
    return shopper

@pytest.fixture
def sample_item():
    item = GroceryItem()
    item.set_item_name("Apple")
    item.set_item_price(1.99)
    return item

@pytest.fixture
def another_item():
    item = GroceryItem()
    item.set_item_name("Banana")
    item.set_item_price(0.99)
    return item

def test_initialization(sample_shopper):
    assert sample_shopper.get_name() == "John Doe"
    assert sample_shopper.get_personal_cart_items() == []
    assert not sample_shopper.get_paid_for_items()
    assert sample_shopper.get_personal_cart_total() == 0.0

def test_add_to_personal_cart(sample_shopper, sample_item):
    sample_shopper.add_to_personal_cart(sample_item)
    assert sample_shopper.get_personal_cart_items() == [sample_item]

def test_remove_from_personal_cart(sample_shopper, sample_item):
    sample_shopper.add_to_personal_cart(sample_item)
    sample_shopper.remove_from_personal_cart(sample_item)
    assert sample_shopper.get_personal_cart_items() == []

def test_remove_from_personal_cart_item_not_found(sample_shopper, sample_item):
    with pytest.raises(ValueError, match="Item not Found in cart."):
        sample_shopper.remove_from_personal_cart(sample_item)

def test_calculate_cart_total(sample_shopper, sample_item, another_item):
    sample_shopper.add_to_personal_cart(sample_item)
    sample_shopper.add_to_personal_cart(another_item)
    assert sample_shopper.calculate_cart_total() == 2.98

def test_set_paid_for_items(sample_shopper):
    sample_shopper.set_paid_for_items(True)
    assert sample_shopper.get_paid_for_items()

def test_set_personal_cart_total(sample_shopper):
    sample_shopper.set_personal_cart_total(15.99)
    assert sample_shopper.get_personal_cart_total() == 15.99

def test_str_representation(sample_shopper, sample_item, another_item):
    sample_shopper.add_to_personal_cart(sample_item)
    sample_shopper.add_to_personal_cart(another_item)
    expected_str = (
        "Shopper: John Doe\n"
        "Personal Cart Items:\n"
        "Apple | $1.99\n"
        "Banana | $0.99\n"
        "Cart Total: $2.98\n"
    )
    assert str(sample_shopper) == expected_str

def test_repr_representation(sample_shopper, sample_item, another_item):
    sample_shopper.add_to_personal_cart(sample_item)
    sample_shopper.add_to_personal_cart(another_item)
    expected_repr = (
        "Shopper(name=John Doe, paid=False, cart_total=0.0)\n"
        "Personal Cart Items:\n"
        "Apple | 1.99\n"
        "Banana | 0.99"
    )
    assert repr(sample_shopper) == expected_repr
