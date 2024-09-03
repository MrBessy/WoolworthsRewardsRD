from abc import ABC, abstractmethod
from typing import Dict
from .digital_receipt_interface import DigitalReceiptInterface
from ..grocery_item import GroceryItem

class FactoryInterface(ABC):

    @abstractmethod
    def _create_grocery_items(self, item_dict) -> Dict[str,GroceryItem]:
        pass

    @abstractmethod
    def create_digital_recipet(self, item_obj_dict, total, EDR_discount_bool) -> DigitalReceiptInterface:
        pass

    @abstractmethod
    def set_grocery_dependency(self, grocery_class:GroceryItem) -> None:
        pass

    @abstractmethod
    def set_digital_receipt_dependency(self, digital_receipt_dependency:DigitalReceiptInterface) -> None:
        pass

    @abstractmethod
    def get_grocery_dependency(self) -> GroceryItem:
        pass
    
    @abstractmethod
    def get_digital_receipt_dependency(self) -> DigitalReceiptInterface:
        pass