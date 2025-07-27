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
    def test_add_new_book(self, mock_input, mock_save_books, mock_load_books):
        # Fake that no books currently exist
        mock_load_books.return_value = []

        # Call the function we're testing
        admin.add_new_resource()

        # Check that the function tried to save one book
        mock_save_books.assert_called_once()

        # Grab the book that would’ve been saved
        saved_books = mock_save_books.call_args[0][0]

        # Now check the content
        self.assertEqual(saved_books[0]['title'], 'Python Basics')
        self.assertEqual(saved_books[0]['author'], 'Alice Walker')
