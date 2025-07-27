# test_library.py
# This file tests all the main features of the admin part of the library system.
# We will test adding a book, adding a user, and removing a user.

import unittest  # This is Python's built-in testing tool
from unittest.mock import patch  # This helps us "pretend" user input and function results
import admin  # We're testing functions from the admin.py file

# Testing Add New Book

class TestAdminAddBook(unittest.TestCase):
    # We use @patch to mock input() and the load/save functions
    @patch('admin.load_books')  # Pretend the books list is coming from here
    @patch('admin.save_books')  # Pretend we’re saving the books somewhere
    @patch('builtins.input', side_effect=[
        'Python Basics',  # title
        'Alice Walker',   # author
        'Computing',      # subject
        'English',        # language
        '/books/python.pdf'  # file path
    ])
