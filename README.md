# Woolworths Receipt Divider

## Overview

The Woolworths Receipt Divider is a Python application designed to simplify the process of splitting Woolworths Rewards receipts among up to four shoppers. The application provides a user-friendly graphical interface built with CustomTkinter, allowing users to efficiently manage and divide their grocery expenses.

## Features

- **Shopper Registration**: Allows users to register up to four shoppers per receipt.
- **Receipt Division**: Automatically divides a loaded Woolworths Rewards receipt, assigning items to the appropriate shoppers.
- **Summary Generation**: Summarizes the receipt to show which shopper owes money or is owed by another.

## Project Structure

The project is organized as follows:

- **app_flow_manager.py**: Manages the application's flow, coordinating interactions between various components.
- **custom_tkinter_gui.py**: Implements the graphical user interface using CustomTkinter, allowing users to interact with the application.
- **digital_receipt.py**: Handles the processing of digital receipts, including extracting items and prices.
- **grocery_item.py**: Represents individual grocery items with attributes like name, price, and quantity.
- **pdf_reader.py**: Provides functionality to read and process PDF files, extracting relevant data for the application.
- **receipt_grocery_factory.py**: Implements the factory pattern to create grocery items from receipt data.
- **shopper.py**: Manages shopper information, including the items they are responsible for.
- **txt_file_handler.py**: Handles the reading and writing of text files for storing shopping data.

### Interfaces

Each class in the project, except for the GUI, has an associated interface file that defines the contract for the class, ensuring that each class adheres to a specific structure and behavior.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/MrBessy/WoolworthsRewardsRD.git
    cd WoolworthsRewardsRD
    ```

2. **Install dependencies**:

    You need to manually install the required dependencies as there is no `requirements.txt` file yet. Here are some of the main dependencies you might need to install:

    ```bash
    pip install customtkinter
    pip install PyPDF2
    ```

3. **Run the application**:

    ```bash
    python -m src.GUI.custom_tkinter_gui
    ```

## Usage

1. **Register Shoppers**: Use the GUI to register up to four shoppers.
2. **Load a Receipt**: Load a Woolworths Rewards receipt file (PDF or text).
3. **Divide the Receipt**: The application will divide the receipt items among the registered shoppers.
4. **Review and Summarize**: Review the summary to see which shopper owes each other, and save the results if needed.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries or support, feel free to reach out at [joshuascattini93@gmail.com](mailto:joshuascattini93@gmail.com).
