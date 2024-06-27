from abc import ABC, abstractmethod

class DigitalReceiptInterface(ABC):

    @abstractmethod
    def calculate_receipt_total(self) -> None:
        pass