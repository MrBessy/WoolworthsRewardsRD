from abc import ABC, abstractmethod

class PDFReaderInterface(ABC):

    @abstractmethod
    def data_process(self, file_locatiom) -> None:
        pass

    @abstractmethod
    def _read_file(self) -> list:
        pass

    @abstractmethod
    def _identify_and_sort_item_lines(self, raw_data_lines) -> None:
        pass

    @abstractmethod
    def _locate_and_adjust_for_discounts(self, sorted_lines: list) -> None:
        pass

    @abstractmethod
    def _locate_receipt_total(self, raw_data_lines: list) -> None:
        pass

    @abstractmethod
    def _identify_line_item(self, adjusted_line: str) -> str:
        pass

    @abstractmethod
    def _identify_line_value(self, adjusted_line: str) -> float:
        pass

    @abstractmethod
    def get_items_dict(self) -> dict:
        pass

    @abstractmethod
    def get_receipt_total(self) -> float:
        pass

    @abstractmethod
    def get_EDR_discount_found(self) -> bool:
        pass

    @abstractmethod
    def set_file_location(self, new_file_location) -> None: 
        pass