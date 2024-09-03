from .interfaces import DigitalReceiptInterface

class DigitalReceipt(DigitalReceiptInterface):
    """
    Class representing a woolworths receipt, extracted from a PDF receipt file.

    Attributes:
    - __receipt_items (dict): Dictionary of receipt items.
    - __receipt_total (float): Total cost of items in the receipt.
    - __everyday_extra_discount (float): Extra discount applied to items if specified."""



    def __init__(self):
        """
        Initialize the Receipt object.
        """
        
        self.__receipt_items = None
        self.__receipt_total = None
        self.__everyday_extra_discount = 0.0

    def get_receipt_items(self) -> dict:
        """Returns the items inside the receipt."""
        
        return self.__receipt_items

    def get_receipt_total(self) -> float:
        """Returns the receipt total."""
        
        return self.__receipt_total
    
    def get_everyday_extra_discount(self) -> float:
        """Get the everyday extra discount applied."""

        return self.__everyday_extra_discount
    
    def set_receipt_total(self, new_total: float) -> None:
        """Sets the receipt total with float number passed"""
        self.__receipt_total = new_total

    def set_receipt_items(self, new_receipt_items: dict) -> None:
        self.__receipt_items = new_receipt_items

    def set_EDR_discount_found(self, EDR_bool: bool) -> None:
        
        if EDR_bool == False:
            self.__everyday_extra_discount = 0.0
        
        else:           # Set and apply discount
            self.__everyday_extra_discount = 0.9
            self.recalculate_items_price(self.__everyday_extra_discount)
            self.calculate_receipt_total(True)
    
    def calculate_receipt_total(self, set_new_total=False) -> None:
        """Calculates the receipt total using the items in the receipt.
            Accepts a parameter of 'True' that will automatically record the calculated total,
            ortherwise it will return the total."""
        
        receipt_total = 0.0
        for obj in self.get_receipt_items().values():
            receipt_total += obj.get_item_price()

        if set_new_total != True:
            return receipt_total
        elif set_new_total == True:
            self.set_receipt_total(receipt_total)

    def recalculate_items_price(self, discount_to_apply) -> None:
        """Recalculate the total cost of items for the discount that is passed."""

        for item in self.get_receipt_items().values():  
                
            # Checks to see if the item is a giftcard
            if "Giftcard" not in item.get_item_name():
                discounted_price = float("%.2f" % (item.get_item_price() * discount_to_apply))
                item.set_item_price(discounted_price)

    def __str__(self) -> str:
        '''
        Returns a friendly representation of the Receipt Class.
        '''

        boarder = "=================================="
        item_num = 1

        return_str = f"\n{boarder*2}\n"
        return_str += f"Number of items in receipt: {len(self.get_receipt_items())}\n"

        # Loop through the receipt items and add them to the return string
        for obj in self.get_receipt_items().values():
            return_str += f"\nItem number: {item_num}\n"
            return_str += str(obj)
            item_num += 1

        return_str += f"\nTotal: ${float('%.2f' % (self.get_receipt_total()-self.get_everyday_extra_discount()))}\n"

        # Check if an everyday extra discount was applied, and alters sting accordingly
        if self.get_everyday_extra_discount() != 0.0:
            return_str += f"\nAfter Everyday Extra Discount of ${-self.get_everyday_extra_discount()} is applied, " +\
            f"new total is: ${self.recalculate_receipt_total()}.\n"

        return_str += f"{boarder*2}"

        return return_str

    def __repr__(self) -> str:
        '''
        Return a string representation of the Receipt class.
        '''
        
        # Loop through the receipt items and add them to the return string
        return_str = f"{len({self.get_receipt_items()})}, " + \
                     f"{', '.join(item.get_item_name() for item in self.get_receipt_items())}, " + \
                     f"{self.get_receipt_total()}"
        
         # Check if an everyday extra discount was applied, and alters sting accordingly
        if self.get_everyday_extra_receipt() != 0.0:
            return_str += f", {self.get_everyday_extra_receipt()}, " +\
                        f"{self.get_receipt_total()-self.get_everyday_extra_receipt()}"

        return return_str

