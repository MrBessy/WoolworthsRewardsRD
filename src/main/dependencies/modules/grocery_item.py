class GroceryItem():
    """
    Class used to store data extracted from a PDF file.

    Attributes:
    - __item_name (str): Name of the grocery item.
    - __item_price (float): Price of the grocery item.

    Methods:
    - get_item_name: Get the name of the grocery item.
    - get_item_price: Get the price of the grocery item.
    - __eq__: Evaulates an instance of this class against another.
    - __str__: Return an interface-friendly string of the item.
    - __repr__: Return the data associated with the item.
    """

    def __init__(self):
        """
        Initialize the GroceryItem object.
        """
        
        self.__item_name = None
        self.__item_price = None

    def get_item_name(self) -> str:
        """Returns the name of the item."""
        return self.__item_name
    
    def get_item_price(self) -> float:
        """"Returns the price of the item."""
        return self.__item_price

    def set_item_name(self, new_name: str) -> None:
        """Sets the price of the item."""
        self.__item_name = new_name

    def set_item_price(self, new_price: float) -> None:
        """Sets the price of the item."""
        self.__item_price = new_price
    
    def __eq__(self, other):
        """Evaulates an instance of this class against another."""
        if isinstance(other, GroceryItem):
            return (self.get_item_name() == other.get_item_name() and
                    self.get_item_price() == other.get_item_price())
        return False
    
    def __str__(self):
        """Return an interface-friendly string of the item."""

        grocery_item_str = f"Product:\t{self.get_item_name()}\nPrice: \t\t" + \
                           f"${self.get_item_price():.2f}\n"

        return grocery_item_str

    def __repr__(self):
        """Return the data associated with the item."""
        grocery_item_repr = f"GroceryItem('{self.get_item_name()}', {self.get_item_price()})"

        return grocery_item_repr
