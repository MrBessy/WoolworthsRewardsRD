from abc import ABC, abstractmethod
from typing import List, Dict
from ..dependencies.modules.interfaces import ShopperInterface, DigitalReceiptInterface

class ManagerInterface(ABC):

    @abstractmethod
    def create_shopper(self, shopper_name) -> ShopperInterface:
        pass

    @abstractmethod
    def get_shopper_dict(self) -> Dict[str,ShopperInterface]:
        pass
    
    @abstractmethod
    def retreive_exisitng_shoppers(self, file_location) -> List[ShopperInterface]:
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
