from .interfaces import TxtFileHandlerInterface

class TxtFileHandler(TxtFileHandlerInterface):
    """
    A class for handling operations with text files, implementing TxtFileHandlerInterface.

    This class provides methods to read from and write to text files. It handles
    common file-related errors such as FileNotFoundError and IOError, providing
    appropriate error messages when encountered.
    """


    def read_from_file(self, file_path) -> list:
        """
        Read lines from a text file and return them as a list of strings.

        Args:
            file_path (str): The path to the text file to read.

        Returns:
            list: A list of strings, each representing a line from the file.
        """
        
        list_of_contents = []

        try: 
            with open(file_path, 'r') as txt_file:
                for line in txt_file:
                    list_of_contents.append(line.strip())
        except FileNotFoundError:
            print(f"The file at {file_path} was not found.")
        
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")

        return list_of_contents

    def write_to_file(self, file_path, list_of_contents) -> None:
        """
        Write a list of strings to a text file.

        Args:
            file_path (str): The path to the text file to write.
            list_of_contents (list): The list of strings to write to the file.
        """
        try:
            with open(file_path, 'w') as txt_file:
                for line in list_of_contents:
                    txt_file.write(line + '\n')
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")