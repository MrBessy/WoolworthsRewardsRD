from abc import ABC, abstractmethod
from .digital_receipt_interface import DigitalReceiptInterface
from ..grocery_item import GroceryItem

class FactoryInterface(ABC):

    @abstractmethod
    def _create_grocery_items(self, item_dict) -> dict[str:GroceryItem]:
        pass

    @abstractmethod
    def create_digital_recipet(self, item_obj_dict, total, EDR_discount_bool) -> DigitalReceiptInterface:
        pass