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

    @abstractmethod
    def set_name(self, new_name) -> None:
        pass

    @abstractmethod
    def get_personal_cart_total(self) -> float:
        pass

    @abstractmethod
    def set_personal_cart_total(self, new_total: float) -> None:
        pass

    @abstractmethod
    def get_paid_for_items(self) -> bool:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_personal_cart_items(self) -> list:
        pass