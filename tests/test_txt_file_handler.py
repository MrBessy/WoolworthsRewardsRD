# tests/test_TxtFileHandler

import pytest
from unittest.mock import mock_open, patch
from src.main.dependencies.modules import TxtFileHandler

@pytest.fixture
def txt_file_handler():
    return TxtFileHandler()

@pytest.fixture
def txt_file_for_testing():
    return "../WoolworthsRewardsRD/tests/txt_file_for_testing.txt"

def test_write_to_file(txt_file_handler, txt_file_for_testing):
    contents_to_write = ['Line 1', 'Line 2', 'Line 3']
    
    # Write to file
    txt_file_handler.write_to_file(txt_file_for_testing, contents_to_write)
    
    # Check that the file was written correctly
    with open(txt_file_for_testing, 'r') as f:
        lines = f.readlines()
        assert len(lines) == len(contents_to_write)
        for i, line in enumerate(lines):
            assert line.strip() == contents_to_write[i]

def test_read_from_file(txt_file_handler, txt_file_for_testing):
    contents_to_write = ['Line 1', 'Line 2', 'Line 3']
    
    # Create the file and write content to it
    with open(txt_file_for_testing, 'w') as f:
        for line in contents_to_write:
            f.write(line + '\n')
    
    # Read from file
    read_lines = txt_file_handler.read_from_file(txt_file_for_testing)
    
    # Check that the lines were read correctly
    assert len(read_lines) == len(contents_to_write)
    for i, line in enumerate(read_lines):
        assert line == contents_to_write[i]

def test_read_nonexistent_file(txt_file_handler):
    # Define a nonexistent file path
    file_path = "nonexistent_file.txt"
    
    # Try reading the file
    read_lines = txt_file_handler.read_from_file(file_path)
    
    # Check that no lines were read
    assert read_lines == []


def test_write_to_file_io_error(txt_file_handler, monkeypatch, capfd):
    m = mock_open()
    m.side_effect = IOError("Unable to open file")

    with patch("builtins.open", m):
        txt_file_handler.write_to_file("/invalid/path/txt_file_for_testing.txt", ["Line 1", "Line 2"])

    captured = capfd.readouterr()
    assert "An error occurred while writing to the file: Unable to open file" in captured.out