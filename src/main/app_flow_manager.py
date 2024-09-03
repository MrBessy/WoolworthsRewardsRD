from .dependencies import DependencyContainer
from .dependencies.modules.interfaces import ShopperInterface, DigitalReceiptInterface, PDFReaderInterface, FactoryInterface, TxtFileHandlerInterface
from .src_interfaces import ManagerInterface
from typing import List, Dict, Tuple

class AppFlowManager(ManagerInterface):

    def __init__(self):
        
        dependency_injector = DependencyContainer()
        self.__scanner = dependency_injector.get_dependency("PDFReaderInterface")
        self.__file_handler = dependency_injector.get_dependency("TxtFileHandlerInterface")
        self.__factory = dependency_injector.get_dependency("FactoryInterface")
        self.__factory.set_digital_receipt_dependency(dependency_injector.get_dependency("DigitalReceiptInterface"))
        self.__digital_receipt = dependency_injector.get_dependency("DigitalReceiptInterface")
        self.__factory.set_grocery_dependency(dependency_injector.get_dependency("GroceryItem"))
        self.__shopper_blueprint = dependency_injector.get_dependency("ShopperInterface")
        self.__shopper_DB_path = dependency_injector.get_dependency("TxtDBFilePath")

        self.__shopper_dict = {}
        self.__shoppers_in_receipt = []
        self.__digital_receipt = None
        
        shared_cart = dependency_injector.get_dependency("ShopperInterface")()
        shared_cart.set_name("Shared")
        self.__shared_cart = shared_cart

    def get_scanner(self) -> PDFReaderInterface:
        return self.__scanner
    
    def get_receipt_content_factory(self) -> FactoryInterface:
        return self.__factory
    
    def get_file_handler(self) -> TxtFileHandlerInterface:
        return self.__file_handler
    
    def get_shopper_blueprint(self) -> ShopperInterface:
        return self.__shopper_blueprint
    
    def get_shopper_DB_path(self) -> str:
        return self.__shopper_DB_path
    
    def get_shopper_dict(self) -> Dict[str,ShopperInterface]:
        return self.__shopper_dict
    
    def get_shared_cart(self) -> ShopperInterface:
        return self.__shared_cart
    
    def get_digital_receipt(self) -> DigitalReceiptInterface:
        return self.__digital_receipt
    
    def set_digital_receipt(self, digital_receipt: DigitalReceiptInterface) -> None:
        self.__digital_receipt = digital_receipt
    
    def set_shoppers_dict(self, new_shoppers_dict) -> None:
        self.__shopper_dict = new_shoppers_dict

    def add_to_shoppers_dict(self, shopper_obj:ShopperInterface) -> None:
        shopper_name = shopper_obj.get_name() 
        self.__shopper_dict[shopper_name] = shopper_obj

    def get_shoppers_in_receipt(self) -> List[str]:
        return self.__shoppers_in_receipt
    
    def set_shoppers_in_receipt(self, new_shopper_list: List) -> None:
        self.__shoppers_in_receipt = new_shopper_list

    def add_shopper_to_receipt(self, shopper_obj:ShopperInterface) -> None:
        self.get_shoppers_in_receipt().append(shopper_obj)

    def create_shopper(self, shopper_name:str) -> ShopperInterface:
        new_shopper = self.get_shopper_blueprint()()
        new_shopper.set_name(shopper_name)

        return new_shopper
    
    def reset_shoppers_variables(self) -> None:
        self.reset_shoppers_items_in_cart()
        self.reset_shoppers_cart_total()
        self.reset_paid_status()
        
    def reset_paid_status(self) -> None:
        for shopper in self.get_shoppers_in_receipt():
                shopper.set_paid_for_items(False)

    def reset_shoppers_items_in_cart(self) -> None:
        for shopper in self.get_shoppers_in_receipt():
                shopper.reset_personal_cart()
        
    def reset_shoppers_cart_total(self) -> None:
        for shopper in self.get_shoppers_in_receipt():
                shopper.set_personal_cart_total(0)

    def retreive_exisitng_shoppers(self, file_location) -> List[ShopperInterface]:
        
        retreived_shoppers = self.get_file_handler().read_from_file(file_location)
        return retreived_shoppers
    
    def save_shopper_info(self, list_of_shoppers:List) -> None:
        
        shoppers_to_store = []
        try:
            if len(self.get_shopper_dict()) <= 0:
                raise ValueError("There are no registered shoppers in shopper_dict.")
    
            for name in self.get_shopper_dict().keys():
                shoppers_to_store.append(name)

            self.get_file_handler().write_to_file(self.get_shopper_DB_path(), shoppers_to_store)
        
        except ValueError as e:
            print(e)

    
    def scan_receipt(self, receipt_file_location) -> DigitalReceiptInterface:
        
        scanner = self.get_scanner()
        scanner.set_file_location(receipt_file_location)
        scanner.data_process()

        factory = self.get_receipt_content_factory()
        digital_receipt = factory.create_digital_recipet(scanner.get_items_dict(), 
                                                         scanner.get_receipt_total(), scanner.get_EDR_discount_found())
        
        for item in digital_receipt.get_receipt_items().values():        
            self.get_shared_cart().add_to_personal_cart(item)
        self.set_digital_receipt(digital_receipt)

        return digital_receipt

    
    def calculate_owings(self, shoppers:List[str]) -> Tuple[str, float]:
        
        shared_cart_total = self.get_shared_cart().get_personal_cart_total()
        shared_cost = shared_cart_total / len(shoppers)
        for shopper in shoppers:
            self.get_shopper_dict()[shopper].set_personal_cart_total(
                self.get_shopper_dict()[shopper].get_personal_cart_total() + shared_cost)

            if self.get_shopper_dict()[shopper].get_paid_for_items() is True:
                shopper_is_owed = self.get_digital_receipt().get_receipt_total() - (self.get_shopper_dict()[shopper].calculate_cart_total() + shared_cost)
                shopper_owed = self.get_shopper_dict()[shopper].get_name()
                
        return shopper_owed, shopper_is_owed
    
