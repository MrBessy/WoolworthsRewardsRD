import pytest
from src.main.dependencies.modules import DigitalReceipt, GroceryItem

@pytest.fixture
def sample_item1():
    item = GroceryItem()
    item.set_item_name("Apple")
    item.set_item_price(1.99)
    return item
    


@pytest.fixture
def sample_item2():
    item = GroceryItem()
    item.set_item_name("Banana")
    item.set_item_price(4.99)
    return item
  

@pytest.fixture
def sample_item3():
    item = GroceryItem()
    item.set_item_name("Bread")
    item.set_item_price(5.0)
    return item

@pytest.fixture
def sample_item4():
    item = GroceryItem()
    item.set_item_name("Ice-Cream")
    item.set_item_price(10.0)
    return item

@pytest.fixture
def items_pack1(sample_item1, sample_item2):
    return {sample_item1.get_item_name(): sample_item1, sample_item2.get_item_name(): sample_item2}

@pytest.fixture
def items_pack2(sample_item3, sample_item4):
    return {sample_item3.get_item_name(): sample_item3, sample_item4.get_item_name(): sample_item4}

@pytest.fixture
def total_pack1(items_pack1):
    return sum(item.get_item_price() for item in items_pack1.values())

@pytest.fixture
def total_pack2(items_pack2):
    return sum(item.get_item_price() for item in items_pack2.values())

def test_initialization_without_discount(items_pack1, total_pack1):
    receipt = DigitalReceipt()
    receipt.set_receipt_items(items_pack1)
    receipt.set_receipt_total(total_pack1)

    assert receipt.get_receipt_items() == items_pack1
    assert receipt.get_receipt_total() == total_pack1
    assert receipt.get_everyday_extra_discount() == 0.0

def test_initialization_with_discount(items_pack2, total_pack2):
    
    receipt = DigitalReceipt()
    receipt.set_receipt_items(items_pack2)
    receipt.set_receipt_total(total_pack2)
    receipt.set_EDR_discount_found(True)

    # Upon initiliazation the disocunt automatically is applied to items
    total_without_discount = 15.0

    assert receipt.get_receipt_items() == items_pack2
    assert receipt.get_receipt_total() == total_without_discount * receipt.get_everyday_extra_discount() # $15 * 0.9 (10% discount) = $13.5

def test_recalculate_items_price(items_pack1, total_pack1):
    receipt = DigitalReceipt()
    receipt.set_receipt_items(items_pack1)
    receipt.set_receipt_total(total_pack1)
    
    
    receipt.recalculate_items_price(0.9)
    
    assert receipt.get_receipt_items()["Apple"].get_item_price() == pytest.approx(1.79)  # 1.99 * 0.9
    assert receipt.get_receipt_items()["Banana"].get_item_price() == pytest.approx(4.49)  # 4.99 * 0.9

def test_set_receipt_total(items_pack2,total_pack2):
    receipt = DigitalReceipt()
    receipt.set_receipt_items(items_pack2)
    receipt.set_receipt_total(total_pack2)

    new_total = 20.0
    receipt.set_receipt_total(new_total)
    
    assert receipt.get_receipt_total() == new_total

def test_calculate_receipt_total(items_pack2, total_pack2):
    receipt = DigitalReceipt()
    receipt.set_receipt_items(items_pack2)
    receipt.set_receipt_total(total_pack2)

    receipt.calculate_receipt_total(set_new_total=True)
    
    assert receipt.get_receipt_total() == total_pack2