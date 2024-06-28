from .interfaces import FactoryInterface
from .digital_receipt import DigitalReceipt
from .grocery_item import GroceryItem

class ReceiptContentsFactory(FactoryInterface):
    """Factory class for creating grocery items and digital receipts."""

    def _create_grocery_items(self, item_dict) -> dict[str:GroceryItem]:
        """
        Create and return a dictionary of GroceryItem instances from item_dict.

        Args:
            item_dict (dict): Dictionary where keys are item names (str) and values are item prices (float).

        Returns:
            dict[str, GroceryItem]: Dictionary where keys are item names and values are GroceryItem instances.
        """
        prepped_item_dictionary = {}
        for item_name, item_price in item_dict.items():
            prepped_item_dictionary[item_name] = GroceryItem(item_name, item_price)

        return prepped_item_dictionary


    def create_digital_recipet(self, item_dict, total, EDR_discount_bool) -> DigitalReceipt:
        """
        Create and return a DigitalReceipt instance.

        Args:
            item_dict (dict): Dictionary where keys are item names (str) and values are item prices (float).
            total (float): Total amount of the receipt.
            EDR_discount_bool (bool): Boolean indicating if EDR discount is applied.

        Returns:
            DigitalReceipt: Instance of DigitalReceipt initialized with created items, total, and EDR discount flag.
        """

        created_items = self._create_grocery_items(item_dict)
        receipt = DigitalReceipt(created_items, total, EDR_discount_bool)

        return receipt