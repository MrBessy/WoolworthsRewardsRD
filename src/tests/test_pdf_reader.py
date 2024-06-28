# test/test_PDFReader

import pytest
from src.modules import PDFReader

@pytest.fixture
def pdf_reader():
    return PDFReader(file_location="test_receipt.pdf")

@pytest.fixture
def pdf_file_location():
    return 'src/tests/pdf_test_receipts/eReceipt_5799_Mawson Lakes_06Jan2024__kdusv.pdf'

def test_initialization(pdf_reader):
    assert pdf_reader.get_file_location() == "test_receipt.pdf"
    assert pdf_reader.get_items_dict() == {}
    assert pdf_reader.get_receipt_total() == 0.0
    assert not pdf_reader.get_EDR_discount_found()
    assert pdf_reader.get_header_rows() == 4

def test_set_file_location(pdf_reader):
    new_location = "new_receipt.pdf"
    pdf_reader.set_file_location(new_location)
    assert pdf_reader.get_file_location() == new_location

def test_set_items_dict(pdf_reader):
    items_dict = {"Apple": 1.99, "Banana": 0.99}
    pdf_reader.set_items_dict(items_dict)
    assert pdf_reader.get_items_dict() == items_dict

def test_set_receipt_total(pdf_reader):
    new_total = 10.0
    pdf_reader.set_receipt_total(new_total)
    assert pdf_reader.get_receipt_total() == new_total

def test_set_EDR_discount_found(pdf_reader):
    pdf_reader.set_EDR_discount_found(True)
    assert pdf_reader.get_EDR_discount_found()

def test_read_file(pdf_file_location, pdf_reader):
    
    pdf_reader.set_file_location(pdf_file_location)

    # Call the method to read the file
    lines = pdf_reader._read_file(pdf_reader.get_file_location())
    # Assert that lines are correctly read from the PDF file
    assert isinstance(lines, list)
    assert len(lines) > 0
    
    assert "Chobani FiT Yogurt Strawberry 680g                 7.50" in lines[10]
    assert "Cadbury Baking Choc Dark Chips 200g                5.00" in lines[13]
    assert "Carrot 1kg P/P                                     1.70" in lines[15]

def test_identify_line_item(pdf_reader):
    line = "Apple  1.99"
    item = pdf_reader._identify_line_item(line)
    assert item == "Apple"

def test_identify_line_value(pdf_reader):
    line = "Apple  1.99"
    value = pdf_reader._identify_line_value(line)
    assert value == 1.99

def test_identify_and_sort_item_lines(pdf_reader):
    raw_data_lines = [
       
        "Header",   # To replicate the receipt header
        "Header",   #
        "Header",   #
        "Header",   #

        "Apple  1.99",
        "Banana  0.99",
        "SUBTOTAL"
    ]

    sorted_lines = pdf_reader._identify_and_sort_item_lines(raw_data_lines)
    assert sorted_lines == ["Apple  1.99", "Banana  0.99"]

def test_locate_and_adjust_for_discounts(pdf_reader):
    sorted_lines = [
        "Apple  1.99",
        "Banana  0.99",
        "Member Price Saving  0.10",
        "Everyday Extra Discount  0.20"
    ]
    adjusted_lines = pdf_reader._locate_and_adjust_for_discounts(sorted_lines)
    assert adjusted_lines == ["Apple  1.99", "Banana  0.89"]

def test_locate_receipt_total(pdf_reader):
    raw_data_lines = [
        "Header",   # To replicate the receipt header
        "Header",   #
        "Header",   #
        "Header",

        "Line1",
        "Line2",
        " TOTAL  10.00"
    ]
    pdf_reader._locate_receipt_total(raw_data_lines)
    assert pdf_reader.get_receipt_total() == 10.0