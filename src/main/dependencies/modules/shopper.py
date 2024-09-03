from .interfaces import ShopperInterface
from .grocery_item import GroceryItem


class Shopper(ShopperInterface):
    """
    Class representing a shopper with a stake in dividing a receipt.

    Attributes:
    - __name (str): The name of the shopper.
    - __personal_cart_items (list): List of grocery items in the shopper's personal cart.
    - __paid_for_items (bool): Indicates if the shopper has paid for the total in store.
    - __cart_total (float): Total cost of items in the shopper's cart."""

    def __init__(self):
        """Initialize the Shopper object."""
        self.__name = None
        self.__personal_cart_items = []
        self.__paid_for_items = False
        self.__personal_cart_total = 0.0

    def get_name(self) -> str:
        """Returns the name of the shopper."""
        return self.__name
    
    def set_name(self, new_name) -> None:
        self.__name =new_name

    def get_personal_cart_items(self) -> list:
        """Returns the cart item objects allocated to the shopper."""
        return self.__personal_cart_items

    def get_paid_for_items(self) -> bool:
        """Returns the cart items allocated to the shopper."""
        return self.__paid_for_items

    def get_personal_cart_total(self) -> float:
        """Returns the cart total of the shopper."""
        return self.__personal_cart_total

    def set_paid_for_items(self, confirmed_paid=True) -> None:
        """Sets the paid boolean of the shopper."""
        self.__paid_for_items = confirmed_paid

    def set_personal_cart_total(self, new_total: float) -> None:
        """Sets the cart total for the shopper."""
        self.__personal_cart_total = new_total

    def add_to_personal_cart(self, item)  -> None:
        """Add a grocery item to the shopper's personal cart.

        Parameters:
        - item: Grocery item object to be added."""

        self.__personal_cart_items.append(item)

    def remove_from_personal_cart(self, item) -> None:
        """Remove an item from the personal cart or reset the cart if specified.

        Parameters:
        - item: Grocery item object to be removed."""

        if item in self.__personal_cart_items:
            self.__personal_cart_items.remove(item)
        else:
            raise ValueError("Item not Found in cart.")

    def reset_personal_cart(self) -> None:
        """Resets personal cart items"""
        self.__personal_cart_items = []

    def calculate_cart_total(self, setter=False) -> float:
        """
        Calculate the total cost of items in the shopper's cart.

        Parameters:
        - setter (bool): If set to True, the cart total is stored.

        Returns:
        - float: Total cost of items in the shopper's cart.
        """

        cart_total = 0.0

        personal_cart_items = self.get_personal_cart_items()

        if personal_cart_items:
            for item_obj in personal_cart_items:
                cart_total += item_obj.get_item_price()
        if setter:
            self.set_personal_cart_total(cart_total)
        return cart_total

    def __str__(self) -> str:
        """
        Return a string representation of the shopper.

        Returns:
        - str: String representation of the shopper.
        """

        shopper_info = f"Shopper: {self.get_name()}\n"

        cart_items_info = "Personal Cart Items:\n"
        for item in self.get_personal_cart_items():
            cart_items_info += f"{item.get_item_name()} | ${item.get_item_price():.2f}\n"

        cart_total_info = f"Cart Total: ${self.calculate_cart_total():.2f}\n"
        shopper_str = f"{shopper_info}{cart_items_info}{cart_total_info}"

        return shopper_str

    def __repr__(self) -> str:
        """
        Returns a string representation of the shopper.

        Returns:
        - str: String representation of the shopper.
        """

        if self.get_personal_cart_items():
            
            cart_items_repr = [f"{item.get_item_name()} | {item.get_item_price()}" for item in self.get_personal_cart_items()]
            
            cart_items_str = "\n".join(cart_items_repr)
            shopper_repr = f"Shopper(name={self.get_name()}, paid={self.get_paid_for_items()}, " \
                        f"cart_total={self.get_personal_cart_total()})\nPersonal Cart Items:\n{cart_items_str}"
        else:
            
            shopper_repr = f"Shopper(name={self.get_name()}, paid={self.get_paid_for_items()}, " \
                        f"cart_total={self.get_personal_cart_total()})\nPersonal Cart Items: No items in cart."

        return shopper_repr

