from abc import ABC, abstractmethod

class ShopperInterface(ABC):

    @abstractmethod
    def add_to_personal_cart(self) -> None:
        pass

    @abstractmethod
    def remove_from_personal_cart(self) -> None:
        pass

    @abstractmethod
    def calculate_cart_total(self) -> float:
        pass
