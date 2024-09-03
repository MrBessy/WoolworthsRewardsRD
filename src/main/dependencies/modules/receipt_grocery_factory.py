from .interfaces import FactoryInterface, DigitalReceiptInterface
from .grocery_item import GroceryItem
from typing import Dict

class ReceiptContentsFactory(FactoryInterface):
    """Factory class for creating grocery items and digital receipts."""

    def __init__(self):
        self.__grocery_item_class = None
        self.__digital_receipt_class = None

    def _create_grocery_items(self, item_dict) -> Dict[str,GroceryItem]:
        """
        Create and return a dictionary of GroceryItem instances from item_dict.

        Args:
            item_dict (dict): Dictionary where keys are item names (str) and values are item prices (float).

        Returns:
            dict[str, GroceryItem]: Dictionary where keys are item names and values are GroceryItem instances.
        """
        prepped_item_dictionary = {}
        for item_name, item_price in item_dict.items():
            new_grocery_class = self.get_grocery_dependency() 
            new_grocery_class.set_item_name(item_name)
            new_grocery_class.set_item_price(item_price)
    
            prepped_item_dictionary[item_name] = new_grocery_class
        return prepped_item_dictionary


    def create_digital_recipet(self, item_dict, total, EDR_discount_bool) -> DigitalReceiptInterface:
        """
        Create and return a DigitalReceipt instance.

        Args:
            item_dict (dict): Dictionary where keys are item names (str) and values are item prices (float).
            total (float): Total amount of the receipt.
            EDR_discount_bool (bool): Boolean indicating if EDR discount is applied.

        Returns:
            DigitalReceipt: Instance of DigitalReceipt initialized with created items, total, and EDR discount flag.
        """

        new_receipt_items = self._create_grocery_items(item_dict)
        receipt = self.get_digital_receipt_dependency()
        receipt.set_receipt_items(new_receipt_items)
        
        receipt.set_receipt_total(total)
        receipt.set_EDR_discount_found(EDR_discount_bool)

        return receipt
    
    
    def set_grocery_dependency(self, grocery_class_dependency:GroceryItem) -> None:
        self.__grocery_item_class = grocery_class_dependency

    def set_digital_receipt_dependency(self, digital_receipt_dependency:DigitalReceiptInterface) -> None:
        self.__digital_receipt_class = digital_receipt_dependency

    def get_grocery_dependency(self) -> GroceryItem:
        if self.__grocery_item_class is None:
            raise ValueError("Grocery item dependency not set")
        return self.__grocery_item_class()

    def get_digital_receipt_dependency(self) -> DigitalReceiptInterface:
        if self.__digital_receipt_class is None:
            raise ValueError("Digital receipt dependency not set")
        return self.__digital_receipt_class