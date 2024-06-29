#tests/AppFlowManager

import pytest
from unittest.mock import MagicMock, patch
from src.main.dependencies import DependencyContainer
#from src.main.src_interfaces import ManagerInterface
from src.main import AppFlowManager

# Mocking the dependencies that AppFlowManager relies on
from src.main.dependencies.modules.interfaces import ShopperInterface, DigitalReceiptInterface, PDFReaderInterface, FactoryInterface, TxtFileHandlerInterface


@pytest.fixture
def mock_dependency_container():
    with patch.object(DependencyContainer, 'get_dependency') as mock_get_dependency:
        # Create mocks for each dependency
        mock_get_dependency.side_effect = lambda name: {
            "PDFReaderInterface": MagicMock(spec=PDFReaderInterface),
            "TxtFileHandlerInterface": MagicMock(spec=TxtFileHandlerInterface),
            "FactoryInterface": MagicMock(spec=FactoryInterface),
            "DigitalReceiptInterface": MagicMock(spec=DigitalReceiptInterface),
            "ShopperInterface": MagicMock(spec=ShopperInterface),
            "GroceryItem": MagicMock(),
            "TxtDBFilePath": 'mock/path/to/db'
        }.get(name, MagicMock())
        yield DependencyContainer()

@pytest.fixture
def app_flow_manager(mock_dependency_container):
    with patch('src.main.app_flow_manager.DependencyContainer', return_value=mock_dependency_container):
        yield AppFlowManager()

def test_initialization(app_flow_manager):
    assert app_flow_manager.get_scanner() is not None
    assert app_flow_manager.get_file_handler() is not None
    assert app_flow_manager.get_receipt_content_factory() is not None
    assert app_flow_manager.get_shopper_blueprint() is not None
    assert app_flow_manager.get_shopper_DB_path() == 'mock/path/to/db'
    assert isinstance(app_flow_manager.get_shopper_dict(), dict)
    assert app_flow_manager.get_shared_cart() is not None
    assert app_flow_manager.get_digital_receipt() is None

def test_create_shopper(app_flow_manager):
    mock_shopper = MagicMock(spec=ShopperInterface)
    mock_shopper.set_name = MagicMock()
    
    with patch.object(app_flow_manager, 'get_shopper_blueprint', return_value=mock_shopper):
        shopper = app_flow_manager.create_shopper("Test Shopper")
        mock_shopper.set_name.assert_called_once_with("Test Shopper")
        assert shopper == mock_shopper

def test_add_to_shoppers_dict(app_flow_manager):
    mock_shopper = MagicMock(spec=ShopperInterface)
    mock_shopper.get_name = MagicMock(return_value="Test Shopper")

    app_flow_manager.add_to_shoppers_dict(mock_shopper)
    assert app_flow_manager.get_shopper_dict()["Test Shopper"] == mock_shopper

def test_scan_receipt(app_flow_manager):
    mock_scanner = MagicMock(spec=PDFReaderInterface)
    mock_factory = MagicMock(spec=FactoryInterface)
    mock_digital_receipt = MagicMock(spec=DigitalReceiptInterface)

    with patch.object(app_flow_manager, 'get_scanner', return_value=mock_scanner):
        with patch.object(app_flow_manager, 'get_receipt_content_factory', return_value=mock_factory):
            mock_scanner.get_items_dict.return_value = {}
            mock_scanner.get_receipt_total.return_value = 100.0
            mock_scanner.get_EDR_discount_found.return_value = False
            mock_factory.create_digital_recipet.return_value = mock_digital_receipt

            digital_receipt = app_flow_manager.scan_receipt('path/to/receipt')

            mock_scanner.set_file_location.assert_called_once_with('path/to/receipt')
            mock_scanner.data_process.assert_called_once()
            mock_factory.create_digital_recipet.assert_called_once_with({}, 100.0, False)
            assert digital_receipt == mock_digital_receipt
            assert app_flow_manager.get_digital_receipt() == mock_digital_receipt

def test_calculate_owings(app_flow_manager):
    mock_shopper1 = MagicMock(spec=ShopperInterface)
    mock_shopper2 = MagicMock(spec=ShopperInterface)
    mock_shopper1.get_personal_cart_total.return_value = 50.0
    mock_shopper2.get_personal_cart_total.return_value = 25.0
    mock_shopper1.get_paid_for_items.return_value = True
    mock_shopper2.get_paid_for_items.return_value = False
    mock_shopper1.get_name.return_value = "Shopper1"
    mock_shopper2.get_name.return_value = "Shopper2"

    mock_digital_receipt = MagicMock(spec=DigitalReceiptInterface)
    mock_digital_receipt.set_receipt_total.return_value = 75.0

    with patch.object(app_flow_manager, 'get_digital_receipt', return_value=mock_digital_receipt):
        app_flow_manager.set_shoppers_dict({"Shopper1": mock_shopper1, "Shopper2": mock_shopper2})
        app_flow_manager.set_shoppers_in_receipt(["Shopper1", "Shopper2"])

        shopper_owed, shopper_is_owed = app_flow_manager.calculate_owings(["Shopper1", "Shopper2"])

        assert shopper_owed == "Shopper1"  # Adjust according to your logic
        assert shopper_is_owed == 25.0  # Adjust according to your logic