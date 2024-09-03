from ..main import AppFlowManager
import customtkinter as CTk
from tkinter import filedialog, LEFT, BOTH, messagebox, RIGHT
from PIL import Image

class WoolworthsReceiptDividerApp:
    def __init__(self):
        CTk.set_appearance_mode('light')
        CTk.set_default_color_theme("green")
        
        self.__background_colour = "#f9f9fa" if CTk.get_appearance_mode() == "Light" else "#343638"

        self.__appManager = AppFlowManager()
        self.__listOfRegisteredShoppers = [] 
        self.__icon_image1 = CTk.CTkImage(light_image=Image.open("src\GUI\images\ReceiptPic.png"), size=(48, 70))
        self.__icon_image2 = CTk.CTkImage(light_image=Image.open("src\GUI\images\ReceiptPic.png"), size=(30, 42))
        
        self.ITEMS_PER_PAGE = 6
        self.__pagination_current_page = 1
        self.__number_of_pagination_pages = 0
        self.__items_in_last_page = 0  
        self.__receipt_path = ""
        self.__selected_shoppers = []
        self.__radio_buttons = []      

        self.__app = CTk.CTk()
        self.__app.title("Woolworths Rewards Receipt Divider")
        self.__app.iconbitmap("src\GUI\images\icon_JS.ico")
        self.__app.geometry('800x500')
        self.__app.resizable(False, False)

    def run(self, page_to_load):
        self.set_list_of_registered_shoppers(self.get_app_manager().retreive_exisitng_shoppers(self.get_app_manager().get_shopper_DB_path()))
        for shopper in self.get_list_of_registered_shoppers():
            obj = self.get_app_manager().create_shopper(shopper)
            self.get_app_manager().add_to_shoppers_dict(obj)
    
        self.show_page(page_to_load)
        self.get_app().mainloop()

    def shutdown(self):
        self.get_app_manager().save_shopper_info(self.get_app_manager().get_shopper_DB_path(), self.get_list_of_registered_shoppers())
    
    def get_pagination_current_page(self):
        return self.__pagination_current_page
    
    def set_pagination_current_page(self, new_page:int):
        self.__pagination_current_page = new_page
    
    def get_items_on_last_page(self):
        return self.__items_in_last_page
    
    def set_items_on_last_page(self, last_items: int):
        self.__items_in_last_page = last_items

    def get_number_of_pagination_pages(self):
        return self.__number_of_pagination_pages
    
    def set_number_of_pagination_pages(self, total_pages):
        self.__number_of_pagination_pages = total_pages

    def get_background_colour(self):
        return self.__background_colour

    def set_background_colour(self, colour):
        self.__background_colour = colour

    def get_app_manager(self):
        return self.__appManager

    def set_app_manager(self, manager):
        self.__appManager = manager

    def get_radio_buttons(self):
        return self.__radio_buttons
    
    def set_radio_buttons(self):
        self.__radio_buttons = []

    def add_radio_buttons(self, button):
        self.__radio_buttons.append(button)

    def get_list_of_registered_shoppers(self):
        return self.__listOfRegisteredShoppers

    def set_list_of_registered_shoppers(self, shoppers):
        self.__listOfRegisteredShoppers = shoppers

    def get_icon_image1(self):
        return self.__icon_image1

    def set_icon_image1(self, image):
        self.__icon_image1 = image

    def get_icon_image2(self):
        return self.__icon_image2

    def set_icon_image2(self, image):
        self.__icon_image2 = image

    def get_app(self):
        return self.__app

    def set_app(self, app):
        self.__app = app

    def get_receipt_path(self):
        return self.__receipt_path
    
    def set_receipt_path(self, receipt_path):
        self.__receipt_path = receipt_path

    def get_selected_shoppers(self):
        return self.__selected_shoppers
    
    def set_selected_shoppers(self, new_list):
        self.__selected_shoppers = new_list

    def split_item_name_into_lines(self, item_name, max_line_length):
        
        words = item_name.split()
        item_lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_line_length:
                current_line += (word + " ")
            else:
                item_lines.append(current_line.strip())
                current_line = word + " "
        item_lines.append(current_line.strip())  # Add the last line
        
        return item_lines

    def display_item_text(self, content_canvas, index, item_lines, y_position, max_line_length):
        item_text = f"{index}. {item_lines[0]}"
        content_canvas.create_text(50, y_position, text=item_text, font=("Helvetica", 10), fill="black", tags="items", anchor="w")
        
        # Handle the second line with truncation and ellipsis if necessary
        if len(item_lines) > 1:
            second_line = item_lines[1]
            if len(second_line) > max_line_length:
                second_line = second_line[:max_line_length - 3] + "..."  # Truncate and add ellipsis
            content_canvas.create_text(65, y_position + 15, text=second_line, font=("Helvetica", 10), tags="items", anchor="w")

    def display_item_price(self, contentCanvas, itemPrice, yPosition):
        contentCanvas.create_text(230, yPosition, text=f"${itemPrice:.2f}", font=("Helvetica", 10), tags="price", anchor="w")


    def cart_handling(self, itemObj, shopperObj):
        
        # Removes item from cart of 1st shopper
        itemRemoved = False
        for shopper in self.get_app_manager().get_shoppers_in_receipt():
            if not itemRemoved:
                for item in shopper.get_personal_cart_items():
                    if itemObj.get_item_name() == item.get_item_name():
                        shopper.remove_from_personal_cart(itemObj)
                        itemRemoved = True
                        break
            else:
                break

        # Adds item to new shopper
        shopperObj.add_to_personal_cart(itemObj)      

    def create_radio_buttons(self, content_canvas, y_position, startPos, SPACE_BETWEEN_SHOPPERS, itemObj):
        
        row_var = CTk.StringVar()
        for shopper_index, shopper in enumerate(self.get_app_manager().get_shoppers_in_receipt()):
            x_position = startPos + (SPACE_BETWEEN_SHOPPERS * shopper_index)
            shopperNameValue = f"{shopper.get_name()}"

            # Create the radio button
            radio_button = CTk.CTkRadioButton(
                content_canvas,
                text="",
                variable=row_var,
                value=shopperNameValue,
                command=lambda item=itemObj, shopper=shopperNameValue: 
                self.cart_handling(item, self.get_app_manager().get_shopper_dict()[shopper]) 
            )

            content_canvas.create_window(x_position, y_position, window=radio_button, anchor="w")
            self.add_radio_buttons(radio_button)

            # Default selection to "Shared" cart
            for item in shopper.get_personal_cart_items():
                if itemObj.get_item_name() == item.get_item_name():
                    row_var.set(shopperNameValue)

    def delete_radio_buttons(self):    
        if self.get_radio_buttons():
            for radio_button in self.get_radio_buttons():
                try:
                    if radio_button.winfo_exists():
                        radio_button.destroy()
                except Exception as e:
                    # Log the exception or handle it appropriately based on your application's needs
                    self.handle_error(f"Error destroying radio button: {str(e)}")
                    
            self.get_radio_buttons().clear()

    def display_items_on_page(self, content_canvas, DR, page_number, next_button, previous_button, startPos, SPACE_BETWEEN_SHOPPERS):
        
        start_index = (page_number - 1) * self.ITEMS_PER_PAGE
        end_index = start_index + self.ITEMS_PER_PAGE

        total_items = len(DR.get_receipt_items())
        items_on_last_page = total_items % self.ITEMS_PER_PAGE
        total_pages = (total_items / self.ITEMS_PER_PAGE) + 1

        if page_number == total_pages:
            end_index = start_index + items_on_last_page  # Adjust for the last page

        items_list = list(DR.get_receipt_items().items())
        items_to_display = items_list[start_index:end_index]

        # Clear existing items and radio buttons on the canvas
        content_canvas.delete("items")
        content_canvas.delete("price")
        self.delete_radio_buttons()

        y_position = 135
        max_line_length = 20
        self.set_radio_buttons()  # To keep track of created radio buttons

        for index, (itemName, itemObj) in enumerate(items_to_display, start=start_index + 1):
            
            item_lines = self.split_item_name_into_lines(itemName,  max_line_length)  
            self.display_item_text(content_canvas, index, item_lines, y_position,  max_line_length)
            self.display_item_price(content_canvas, itemObj.get_item_price(), y_position)
            self.create_radio_buttons(content_canvas, y_position, startPos-10, SPACE_BETWEEN_SHOPPERS, itemObj)

            y_position += 52  # Adjust the y position for the next item

        # Disable/Enable buttons based on the current page
        if page_number <= 1:
            previous_button.configure(state="disabled")
        else:
            previous_button.configure(state="normal")

        if page_number >= total_pages:
            next_button.configure(state="disabled")
        else:
            next_button.configure(state="normal")

    def next_page(self, content_canvas, DR, next_button, previous_button, startPos, SPACE_BETWEEN_SHOPPERS):
        if self.get_pagination_current_page() < self.get_number_of_pagination_pages():
            new_page = self.get_pagination_current_page() + 1 
            self.set_pagination_current_page(new_page)  
            self.display_items_on_page(content_canvas, DR, self.get_pagination_current_page(), next_button, 
                                       previous_button, startPos, SPACE_BETWEEN_SHOPPERS)

            # Check if the current page is the last one, and disable the next button if it is
        if self.get_pagination_current_page() >= self.get_number_of_pagination_pages():
            next_button.configure(state="disabled")
        # Re-enable the previous button if not on the first page
        previous_button.configure(state="normal")

    def previous_page(self, content_canvas, DR, next_button, previous_button, startPos, SPACE_BETWEEN_SHOPPERS):
        if self.get_pagination_current_page() > 1: 
            new_page = self.get_pagination_current_page() - 1  
            self.set_pagination_current_page(new_page) 
            self.display_items_on_page(content_canvas, DR, self.get_pagination_current_page(), next_button, 
                                       previous_button, startPos, SPACE_BETWEEN_SHOPPERS)

        # Check if the current page is the first one, and disable the previous button if it is
        if self.get_pagination_current_page() <= 1:
            previous_button.configure(state="disabled")
        # Re-enable the next button since we moved back a page
        next_button.configure(state="normal")

    def process_request(self):
        
        # Ensures all relevent fields are entered before continuing
        if not self.get_receipt_path():  
            messagebox.showwarning("No Receipt Selected", "Please select a receipt before proceeding.")
            return  

        if not self.are_all_dropdowns_filled():
            messagebox.showwarning("Incomplete Selections", "Please ensure all shopper selections are filled or that the selected shopper is valid.")
            return  
        
        if self.who_paid_var.get() == "Select Payee" or not self.who_paid_var.get():
            messagebox.showwarning("Incomplete Selections", "Please ensure you have selected who made the purchase.")
            return

        # Ensures previous shoppers arent added to new calculation
        self.get_app_manager().set_shoppers_in_receipt([])

        # Ensure shoppers are unique and correctly set
        for shopper in self.get_selected_shoppers():
            if shopper == "":
                continue 
            try:
                shopper_obj = self.get_app_manager().get_shopper_dict()[shopper]
                if shopper == self.who_paid_var.get():
                    shopper_obj.set_paid_for_items()
                self.get_app_manager().add_shopper_to_receipt(shopper_obj)
                

            except KeyError:
                print(f"Shopper {shopper} not found in shopper_dict.")

        self.get_app_manager().add_shopper_to_receipt(self.get_app_manager().get_shared_cart())
        self.get_app_manager().scan_receipt(self.get_receipt_path())
        
        shared_cart = self.get_app_manager().get_shared_cart()
        self.get_app_manager().add_to_shoppers_dict(shared_cart)
        self.show_page('divide_receipt_page')

    def show_page(self, page_name):
        for widget in self.get_app().winfo_children():
            widget.destroy()
        self.delete_radio_buttons()

        if page_name == 'home_page':
            self.get_app_manager().reset_shoppers_variables()
            self.create_home_page()
        elif page_name == 'divide_receipt_page':
            self.create_divide_receipt_page()
        elif page_name == 'results_page':
            
            self.create_results_page()

    def load_receipt_file(self, receipt_full_path, receipt_display_path):
        receipt_path = filedialog.askopenfilename(title="Select Receipt", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
        if receipt_path:
            receipt_full_path.set(receipt_path)
            max_display_length = 35
            shortened_path = "..." + receipt_path[-(max_display_length-3):] if len(receipt_path) > max_display_length else receipt_path
            receipt_display_path.set(shortened_path)

    def update_who_paid_dropdown(self):

        if self.get_selected_shoppers():
            self.who_paid_dropdown.configure(state="readonly")
            self.who_paid_dropdown.configure(values=self.get_selected_shoppers(), fg_color='#f9f9fa')

        else:
            self.who_paid_dropdown.configure(state="disabled", fg_color='#d3d3d3')
            self.who_paid_var.set("Select Payee")

    def update_shopper_dropdowns(self, shoppers_var, shopper_dropdown_frame):
        number_of_shoppers = shoppers_var.get()

        # Clear the selected shoppers list when the number of shoppers changes
        self.set_selected_shoppers([])

        # Clear existing dropdowns
        for widget in shopper_dropdown_frame.winfo_children():
            widget.destroy()

        selectedShoppers = self.get_selected_shoppers()

        # Function to handle selection change
        def on_selection_change(var, prev_value):
            selected_shopper = var.get()
            
            # Remove the previous selection from the selected list
            if prev_value in selectedShoppers:
                selectedShoppers.remove(prev_value)
            
            # Add the new selection to the selected list if it's valid
            if selected_shopper and selected_shopper != "Select Shopper":
                if selected_shopper not in selectedShoppers:
                    selectedShoppers.append(selected_shopper)
            
            # Update the selected shoppers list
            self.set_selected_shoppers(selectedShoppers)
            self.update_who_paid_dropdown()
            refresh_dropdowns()

        # Refresh dropdowns based on current selections
        def refresh_dropdowns():
            for i, var in enumerate(shopper_vars):
                current_selection = var.get()
                available_shoppers = [shopper for shopper in self.get_list_of_registered_shoppers() 
                                      if shopper not in selectedShoppers or shopper == current_selection]
                dropdown = shopper_dropdown_frame.winfo_children()[i]
                dropdown.configure(values=available_shoppers)
                
        shopper_vars = []
        self.set_selected_shoppers(selectedShoppers)

        for i in range(number_of_shoppers):
            shopper_var = CTk.StringVar(value="Select Shopper")
            shopper_vars.append(shopper_var)

            prev_value = [""]  # Use a list to store the previous value

            # Define a callback that captures the previous value before the selection changes
            def callback(var_name, index, mode, v=shopper_var, pv=prev_value):
                on_selection_change(v, pv[0])
                pv[0] = v.get()  # Update the previous value to the current selection

            shopper_dropdown = CTk.CTkComboBox(shopper_dropdown_frame, values=self.get_list_of_registered_shoppers(), variable=shopper_var, state="readonly")
            shopper_dropdown.pack(pady=5)
            shopper_var.trace_add("write", callback)
       
        self.shopper_vars = shopper_vars
        self.update_who_paid_dropdown()

    def add_new_shopper(self, new_shopper_entry, update_dropdowns_callback):
        new_shopper_name = new_shopper_entry.get().strip().lower()
        if new_shopper_name and new_shopper_name != "enter shopper name":
            if new_shopper_name in [shopper.lower() for shopper in self.get_list_of_registered_shoppers()]:
                messagebox.showwarning("Duplicate Entry", f"The shopper '{new_shopper_name.capitalize()}' is already registered.")
            else:
                newObj = self.get_app_manager().create_shopper(new_shopper_name.capitalize())
                self.get_app_manager().add_to_shoppers_dict(newObj)
                current_shoppers = self.get_list_of_registered_shoppers()
                current_shoppers.append(newObj.get_name())
                self.set_list_of_registered_shoppers(current_shoppers)
                self.get_app_manager().save_shopper_info(current_shoppers)
                messagebox.showwarning("Shopper Registered", f"The shopper '{new_shopper_name.capitalize()}' is now registered.")
                update_dropdowns_callback()
        else:
            messagebox.showwarning("Invalid Entry", "Please enter a valid shopper name.")

    def are_all_dropdowns_filled(self):
        for dropdown in self.shopper_dropdown_frame.winfo_children():
            if isinstance(dropdown, CTk.CTkComboBox):
                if dropdown.get() == "Select Shopper" or dropdown.get() == "":
                    return False
        return True

    def create_home_page(self):
        
        content_canvas = CTk.CTkCanvas(self.get_app(), background=self.get_background_colour())
        content_canvas.pack(fill=BOTH, expand=True)

        # Set icon and Labels
        icon_label = CTk.CTkLabel(content_canvas, image=self.get_icon_image1(), text="")
        content_canvas.create_window(400, 60, window=icon_label)

        content_canvas.create_text(400, 120, text="Woolworths Receipt Divider", font=("Helvetica", 25), fill="black")
        content_canvas.create_text(520, 145, text="By Joshua Scattini", font=("Helvetica", 8), fill="black")

        # Recipet Browsing
        receipt_frame = CTk.CTkFrame(content_canvas)
        content_canvas.create_window(400, 180, window=receipt_frame)

        receipt_full_path = CTk.StringVar(value="")
        receipt_display_path = CTk.StringVar(value="")
        receipt_path_label = CTk.CTkLabel(receipt_frame, textvariable=receipt_display_path, width=250, anchor="w", corner_radius=10)
        receipt_path_label.pack(side=LEFT, padx=5)

        browse_button = CTk.CTkButton(receipt_frame, text="Browse", command=lambda: self.load_receipt_file(receipt_full_path, receipt_display_path), 
                                      background_corner_colors=(None, 
                                                                self.get_background_colour(), 
                                                                self.get_background_colour(), 
                                                                None))
        browse_button.pack(side=LEFT, padx=0)

        # Number of Shoppers
        shoppers_label = CTk.CTkLabel(content_canvas, text="Number of Shoppers", font=("Arial", 18))
        content_canvas.create_window(230, 230, window=shoppers_label)

        shoppers_frame = CTk.CTkFrame(content_canvas, fg_color=self.get_background_colour(), border_width=0)
        content_canvas.create_window(235, 260, window=shoppers_frame)

        shoppers_var = CTk.IntVar(value=2)
        shoppers_var.trace_add("write", lambda *args: self.update_shopper_dropdowns(shoppers_var, self.shopper_dropdown_frame))

        for num in range(2, 5):
            shopper_radio_button = CTk.CTkRadioButton(
                shoppers_frame, 
                text=str(num), 
                variable=shoppers_var, 
                value=num, 
                width=50, 
                bg_color=self.get_background_colour(),      
            )
            shopper_radio_button.grid(row=0, column=num-2, padx=2, pady=2)

        self.shopper_dropdown_frame = CTk.CTkFrame(content_canvas, fg_color=self.get_background_colour(), border_width=0, height=150)
        
        content_canvas.create_window(225, 280, window=self.shopper_dropdown_frame, anchor="n")

        # Register Shopper
        new_shopper_label = CTk.CTkLabel(content_canvas, text="Register New Shopper", font=("Arial", 18))
        content_canvas.create_window(550, 360, window=new_shopper_label)

        new_shopper_entry = CTk.CTkEntry(content_canvas, width=180, justify="center", placeholder_text="Enter Shopper Name", fg_color="#DDDFE0")
        content_canvas.create_window(510, 390, window=new_shopper_entry)

        add_shopper_button = CTk.CTkButton(content_canvas, text="Add", 
                                            command=lambda: self.add_new_shopper(new_shopper_entry, 
                                            lambda: self.update_shopper_dropdowns(shoppers_var, self.shopper_dropdown_frame)), width=60)
        content_canvas.create_window(640, 390, window=add_shopper_button)

        # Who Made the Purchase
        self.who_paid_dropdown_frame = CTk.CTkFrame(content_canvas, fg_color=self.get_background_colour(), border_width=0)
    
        self.who_paid_label = CTk.CTkLabel(content_canvas, text="Who Made the Purchase?", font=("Arial", 18))
        content_canvas.create_window(550, 260, window=self.who_paid_label)

        self.who_paid_var = CTk.StringVar(value="Select Payee")
        self.who_paid_dropdown = CTk.CTkComboBox(self.who_paid_dropdown_frame, values=["Select Payee"], variable=self.who_paid_var, state="disabled", width=150)
        self.who_paid_dropdown.pack(pady=10)
        content_canvas.create_window(550, 292, window=self.who_paid_dropdown_frame)

        # Divide Receipt Button
        divide_receipt_button = CTk.CTkButton(content_canvas, text="Divide receipt", 
                                                command=lambda: (self.set_receipt_path(receipt_full_path.get()),
                                                self.process_request()))
        content_canvas.create_window(400, 450, window=divide_receipt_button)
        
        
        self.update_shopper_dropdowns(shoppers_var, self.shopper_dropdown_frame)
        self.update_who_paid_dropdown()

    def create_divide_receipt_page(self):
        list_of_shoppers = self.get_app_manager().get_shoppers_in_receipt()
        NUM_OF_SHOPPERS = len(list_of_shoppers)
        
        # Determine the space between shoppers and the starting position dynamically
        SPACE_BETWEEN_SHOPPERS = 200 - (NUM_OF_SHOPPERS * 20)  # Adjust space based on number of shoppers
        if NUM_OF_SHOPPERS == 3:
            startPos = 390
        elif NUM_OF_SHOPPERS == 4:
            startPos = 350
        else:
            startPos = 330  # Shift more to the left if 4 shoppers

        content_canvas = CTk.CTkCanvas(self.get_app(), background=self.get_background_colour())
        content_canvas.pack(fill=BOTH, expand=True)  # Pack the canvas once

        # Create text and icon as before
        content_canvas.create_text(150, 30, text="Woolworths Receipt Divider", font=("Helvetica", 10, 'bold'), fill="black")
        content_canvas.create_text(175, 43, text="Joshua Scattini", font=("Helvetica", 8), fill="black")
        icon_label = CTk.CTkLabel(content_canvas, image=self.get_icon_image2(), text="")
        content_canvas.create_window(40, 35, window=icon_label)
        
        content_canvas.create_text(80, 90, text="Item", font=("Helvetica", 12, "bold"))
        content_canvas.create_text(248, 90, text="Price", font=("Helvetica", 12, "bold"))

        # Retunr to home page button
        back_button = CTk.CTkButton(content_canvas, text="Back", text_color="black", font=("Helvetica", 12, "underline"), hover_color="#d3d3d3", 
                                    fg_color=self.get_background_colour(), command=lambda: self.show_page('home_page'))
        back_button_window = content_canvas.create_window(720, 35, window=back_button, width=60)

        DR = self.get_app_manager().get_digital_receipt()
        
        # Calculate the number of pages
        total_items = len(DR.get_receipt_items())
        self.set_number_of_pagination_pages((total_items / self.ITEMS_PER_PAGE))

        # Check if the last page would be empty
        items_on_last_page = total_items % self.ITEMS_PER_PAGE
        if items_on_last_page == 0 and total_items > 0:
            self.set_number_of_pagination_pages(self.get_number_of_pagination_pages())

        self.set_pagination_current_page(1)  # Start at the first page

        # Add navigation buttons
        next_button = CTk.CTkButton(content_canvas, text="Next >>", command=lambda: self.next_page(content_canvas, DR, 
                                                                                                   next_button, previous_button,
                                                                                                   startPos, SPACE_BETWEEN_SHOPPERS))
        next_button_window = content_canvas.create_window(600, 450, window=next_button)

        previous_button = CTk.CTkButton(content_canvas, text="<< Previous", command=lambda: self.previous_page(content_canvas, DR, 
                                                                                                               next_button, previous_button,
                                                                                                               startPos, SPACE_BETWEEN_SHOPPERS))
        previous_button_window = content_canvas.create_window(200, 450, window=previous_button)

        # Display the first page of items
        self.display_items_on_page(content_canvas, DR, self.get_pagination_current_page(), next_button, 
                                   previous_button, startPos, SPACE_BETWEEN_SHOPPERS)

        # Submit Button
        submit_button = CTk.CTkButton(content_canvas, text="Calculate!", command=lambda: self.show_page('results_page'))
        submit_button_window = content_canvas.create_window(400, 450, window=submit_button)

        # Loop through the shoppers and display their names
        for index, shopper in enumerate(self.get_app_manager().get_shoppers_in_receipt()):
            x_position = startPos + (SPACE_BETWEEN_SHOPPERS * index)
            content_canvas.create_text(x_position, 90, text=shopper.get_name(), font=("Helvetica", 12), fill="black", justify="center")

        # Initialize buttons as disabled if necessary
        if self.get_pagination_current_page() <= 1:
            previous_button.configure(state="disabled")
        if self.get_pagination_current_page() >= self.get_number_of_pagination_pages():
            next_button.configure(state="disabled")

    def create_results_page(self):
        
        NUM_OF_SHOPPERS = len(self.get_selected_shoppers())
        
        shared_total = self.get_app_manager().get_shopper_dict()['Shared'].calculate_cart_total(True)
        who_paid, amount_owed = self.get_app_manager().calculate_owings(self.get_selected_shoppers())
        startPos = 170
        # Determine the space between shoppers and the starting position dynamically
        SPACE_BETWEEN_SHOPPERS = 60
        
        
        content_canvas = CTk.CTkCanvas(self.get_app(), background=self.get_background_colour())
        content_canvas.pack(fill=BOTH, expand=True)  # Pack the canvas once

        # Create Text and Icon's
        content_canvas.create_text(150, 30, text="Woolworths Receipt Divider", font=("Helvetica", 10, 'bold'), fill="black")
        content_canvas.create_text(175, 43, text="Joshua Scattini", font=("Helvetica", 8), fill="black")
        content_canvas.create_text(400, 70, text="Summary", font=("Helvetica", 18, 'bold'))
        content_canvas.create_text(680, 73, text=f"{who_paid}\n${self.get_app_manager().get_digital_receipt().get_receipt_total()}", 
                                   font=("Helvetica", 10, 'bold'), fill="black", justify='center')
        content_canvas.create_text(560, 73, text=f"Made Purchase:\nReceipt Total:", justify="center", 
                                   font=("Helvetica", 10, 'italic'), fill="black",)    

        icon_label = CTk.CTkLabel(content_canvas, image=self.get_icon_image2(), text="")
        content_canvas.create_window(40, 35, window=icon_label)

        content_canvas.create_text(80, 130, text="Name", font=("Helvetica", 10, 'bold'))
        content_canvas.create_text(200, 130, text="Personal Spend", font=("Helvetica", 10, 'bold'))
        content_canvas.create_text(320, 130, text="Shared Total", font=("Helvetica", 10, 'bold'))
        content_canvas.create_text(440, 130, text="Total Spend", font=("Helvetica", 10, 'bold'))
        content_canvas.create_text(560, 130, text="Amount Owing", font=("Helvetica", 10, 'bold'))
        content_canvas.create_text(680, 130, text="To Receive", font=("Helvetica", 10, 'bold'))

        # Shoppers calculations
        for index, shopper in enumerate(self.get_app_manager().get_shoppers_in_receipt()):
            if shopper.get_name() != "Shared":
                personal_cart_total = shopper.calculate_cart_total()
                y_position = startPos + (SPACE_BETWEEN_SHOPPERS * index)
                total_spend = (shared_total/(NUM_OF_SHOPPERS)) + personal_cart_total
                shared_total_formated = f"{(shared_total/(NUM_OF_SHOPPERS)):.2f}"
                personal_cart_total = f"{personal_cart_total:.2f}"
                total_spend = f"{total_spend:.2f}"

                # Name
                content_canvas.create_text(80, y_position, text=shopper.get_name(), font=("Helvetica", 10), fill="black", justify="center")

                # Personal Spend
                content_canvas.create_text(200, y_position, text=personal_cart_total, font=("Helvetica", 10, 'italic'), fill="black", justify="center")
                # Line For Shared Cart Total
                content_canvas.create_text(320, y_position, text=shared_total_formated, font=("Helvetica", 10, 'italic'), fill="black", justify="center")

                # Total Spend 
                content_canvas.create_text(440, y_position, text=total_spend, font=("Helvetica", 10, 'italic'), fill="black", justify="center")

                # Amount owing
                if shopper.get_name() != who_paid:
                    amount_owing = total_spend
                else:
                    amount_owing = "--"
                content_canvas.create_text(560, y_position, text=amount_owing, font=("Helvetica", 10, 'italic'), fill="black", justify="center")

                # Amont To recieve
                if shopper.get_name() != who_paid:
                    is_owed = "--"
                else:
                    is_owed = f"{amount_owed:.2f}"
                content_canvas.create_text(680, y_position, text=is_owed, font=("Helvetica", 10, 'italic'), fill="black", justify="center")

                # Divide Line
                content_canvas.create_line(50, y_position + 25, 750, y_position + 25, fill="#d3d3d3")
            else: 
                pass

               # Return to divide_receipt_page button
        back_button = CTk.CTkButton(content_canvas, text="Back to Receipt", font=("Helvetica", 12), command=lambda: self.show_page('divide_receipt_page'))
        back_button_window = content_canvas.create_window(200, 450, window=back_button)

        # Return to home_page button
        home_button = CTk.CTkButton(content_canvas, text="Home", font=("Helvetica", 12), command=lambda: self.show_page('home_page'))
        home_button_window = content_canvas.create_window(600, 450, window=home_button)


if __name__ == "__main__":
    app = WoolworthsReceiptDividerApp()
    app.run("home_page")
