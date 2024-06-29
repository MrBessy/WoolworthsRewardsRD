from abc import ABC, abstractmethod
from ..dependencies.modules.interfaces import ShopperInterface, DigitalReceiptInterface

class ManagerInterface(ABC):

    @abstractmethod
    def create_shopper(self, shopper_name) -> ShopperInterface:
        pass
    
    @abstractmethod
    def retreive_exisitng_shoppers(self, file_location) -> list[ShopperInterface]:
        pass

    @abstractmethod
    def save_shopper_info(self, filke_location, list_of_shoppers) -> None:
        pass

    @abstractmethod
    def scan_receipt(self, receipt_file_location) -> DigitalReceiptInterface:
        pass

    @abstractmethod
    def calculate_owings(self, shoppers) -> float:
        pass
