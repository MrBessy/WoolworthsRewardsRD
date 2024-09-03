from abc import ABC, abstractmethod

class DigitalReceiptInterface(ABC):

    @abstractmethod
    def calculate_receipt_total(self) -> None:
        pass

    @abstractmethod
    def get_receipt_total(self) -> float:
        pass

    @abstractmethod
    def set_receipt_items(self, new_receipt_items) -> None:
        pass
    
    @abstractmethod
    def set_receipt_total(self, new_receipt_total) -> None:
        pass

    @abstractmethod
    def set_EDR_discount_found(self, EDR_bool) -> None:
        pass

    @abstractmethod
    def get_receipt_items(self) -> list:
        pass
