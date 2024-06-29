from abc import ABC, abstractmethod

class TxtFileHandlerInterface(ABC):

    @abstractmethod
    def read_from_file(self, file_path) -> list:
        pass

    @abstractmethod
    def write_to_file(self, file_path, list_of_shoppers) -> None:
        pass