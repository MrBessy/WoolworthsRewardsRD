from .modules import DigitalReceipt, PDFReader, ReceiptContentsFactory, Shopper, TxtFileHandler, GroceryItem
from .modules.interfaces import *

class DependencyContainer():
    """
    This class stores dependencies in a dictionary and provides methods for adding, retrieving,
    and initializing them. It also includes a method for initializing specific dependencies
    used within the application.
    """

    def __init__(self):
        self.__dependencies = {}
        self.initialise_dependencies()

    def add_dependency(self, name, dependency):
        self.__dependencies[name] = dependency

    def get_dependency(self, name):
        return self.__dependencies[name]

    def initialise_dependencies(self):
        """
        Initializes the core dependencies for the application.

        It adds and initializes dependencies for object detection, index access, object matching,
        image access, task factory, and task orchestration.
        """

        self.add_dependency('DigitalReceiptInterface', DigitalReceipt())
        self.add_dependency('PDFReaderInterface', PDFReader())
        self.add_dependency('FactoryInterface', ReceiptContentsFactory())
        self.add_dependency('ShopperInterface', Shopper)
        self.add_dependency('TxtFileHandlerInterface', TxtFileHandler())
        self.add_dependency('GroceryItem', GroceryItem)
        self.add_dependency('TxtDBFilePath', '../WoolworthsRewardsRD/src/main/databases/registered_shoppers.txt')
