import fitz # pip install PyMuPDF

from .interfaces import PDFReaderInterface

class PDFReader(PDFReaderInterface):
    """
    A class for reading and processing PDF receipts.

    Attributes:
        __file_location (str): The file location of the PDF receipt.
        __items_dict (dict): Dictionary to store parsed items and their prices.
        __receipt_total (float): Total amount from the receipt.
        __EDR_disount_found (bool): Flag indicating if an Everyday Rewards discount was found.
        __header_row (int): Default header row number for receipts."""

    def __init__(self, header_row=4):
        
        self.__file_location = ""
        self.__items_dict = {}
        self.__receipt_total = 0.0
        self.__EDR_disount_found = False
        self.__header_row = header_row # set to 4 as default for EDR receipts

    def data_process(self) -> None:
        """Process the PDF data to extract items, prices, and total."""

        try:
            if self.get_file_location() == "":
                raise ValueError("File location has not been added and cannot continue.")
        except ValueError as e:
            print(e)
            return
        else:
            
            prepped_data_dict = {}

            raw_lines = self._read_file(self.get_file_location())
            sorted_lines = self._identify_and_sort_item_lines(raw_lines)           
            self._locate_receipt_total(raw_lines)
            adjusted_lines = self._locate_and_adjust_for_discounts(sorted_lines)   # setting ERD disocunt happens here

            for line in adjusted_lines:
                item = self._identify_line_item(line)
                price = self._identify_line_value(line)
                
                # Initialize a counter for the item
                count = 1
                item_name_with_count = item
                
                # Check if the item already exists in the dictionary
                while item_name_with_count in prepped_data_dict:
                    count += 1
                    item_name_with_count = f"{item} #{count}"  # Append the count to the item name
                
                # Add the item with the modified name to the dictionary
                prepped_data_dict[item_name_with_count] = price

            self.set_items_dict(prepped_data_dict)

    
    def _read_file(self, file_location) -> list:
        """Read the PDF file and return lines of text."""

        doc = fitz.open(file_location)

        for page in doc:
            text = page.get_text("text")

        # Split the text into lines
        lines = text.split('\n')

        return lines

    
    def _identify_and_sort_item_lines(self, raw_data_lines) -> list:
        """Identify and sort lines containing item details."""

        items_and_price_list = []
        current_item = None       

        for line in raw_data_lines[self.get_header_rows():]:
            if "SUBTOTAL" in line or "^Promotional Price" in line:
                break

            if line.endswith("  ") and not line.strip().startswith("PRICE REDUCED"):
                current_item = line.strip()

            elif not line.strip().startswith("PRICE REDUCED"):
                
                if current_item:
                    items_and_price_list.append(current_item + "  " + line.strip())
                    current_item = ""
                else:
                    items_and_price_list.append(line.strip())

        if current_item:
            items_and_price_list.append(current_item)

        return items_and_price_list

    
    def _locate_and_adjust_for_discounts(self, sorted_lines) -> list:
        """Locate discounts and adjust item prices accordingly."""

        discount_conditions = ["Member Price Saving", "Everyday Extra Discount", "OFFER", "Everyday Extra Perk", "Offe ", "ANY 2 ", "ANY 3 ", "PRICE REDUCED "]
        lines_to_remove = []
        loop_index = 0

        while loop_index < len(sorted_lines):
            item_line_target = sorted_lines[loop_index]

            # Handles case if discount is found
            if any(discount in item_line_target for discount in discount_conditions):
                discount_found = self._identify_line_value(item_line_target)
                lines_to_remove.append(loop_index)

                #Further handling for specific discount type
                if not item_line_target.startswith("Everyday Extra Discount"):
                    if loop_index !=0:
                        previous_item_line = sorted_lines[loop_index - 1]
                        original_item_price = self._identify_line_value(previous_item_line)

                        if original_item_price is not None:
                            new_price = original_item_price - discount_found

                            #adjust the line price to reflect item price
                            sorted_lines[loop_index -1] = f"{previous_item_line[:-len(str(original_item_price)) - 1].rstrip()}{' ' * 2}{new_price:.2f}"
                
                else:           
                    self.set_EDR_discount_found(True)
                
            loop_index += 1

        for remove_index in sorted(lines_to_remove, reverse=True):
            sorted_lines.pop(remove_index)

        return sorted_lines

    
    def _locate_receipt_total(self, raw_data_lines) -> None:
        """Locate and set the receipt total."""

        for line in raw_data_lines[self.get_header_rows():]:
            if " TOTAL " in line:
                total = self._identify_line_value(line)
                break

        self.set_receipt_total(total)

    def item_line_prep(self, line_to_prep):
        prepped_line = line_to_prep.replace("#", "").replace("^", "").strip()
        return prepped_line 

    def _identify_line_item(self, adjusted_line) -> str:
        """Identify the item name from an adjusted line of text."""

        adjusted_line = adjusted_line.strip()
        line_values = adjusted_line.split("  ")
        item_str = line_values[0]
        item_name = self.item_line_prep(item_str)

        return item_name
    
    def _identify_line_value(self, adjusted_line) -> float:
        """Identify the price value from an adjusted line of text."""

        stripped_line = adjusted_line.strip()
        temp_line = ""
        for char in reversed(stripped_line):
            if char.isdigit() or char == '.':
                temp_line += char
            else:
                break

        # Reverse the string and convert to float
        item_price = float(temp_line[::-1])

        return item_price

    def get_file_location(self) -> str:
        """Get the current file location."""

        return self.__file_location
    
    def set_file_location(self, new_file_location) -> None:
        """Set a new file location."""
        
        self.__file_location = new_file_location

    def get_items_dict(self) -> dict:
        """Get the dictionary of parsed items and prices."""

        return self.__items_dict
    
    def get_receipt_total(self) -> float:
        """Get the total amount from the receipt."""
        
        return self.__receipt_total
    
    def get_EDR_discount_found(self) -> bool:
        """Check if an Everyday Rewards discount was found."""

        return self.__EDR_disount_found

    def get_header_rows(self) -> int:
        """Get the header row number for the receipt."""

        return self.__header_row

    def set_items_dict(self, new_items_dict):
        """Set a new dictionary of items and prices."""

        self.__items_dict = new_items_dict
    
    def set_receipt_total(self, new_receipt_total):
        """Set a new receipt total."""
        
        self.__receipt_total = new_receipt_total
   
    def set_EDR_discount_found(self, EDR_found):
        """Set the flag indicating an Everyday Rewards discount."""
        
        self.__EDR_disount_found = EDR_found
