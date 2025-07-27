# test_library.py
# This file tests all the main features of the admin part of the library system.
# We will test adding a book, adding a user, and removing a user.

import unittest  # This is Python's built-in testing tool
from unittest.mock import patch  # This helps us "pretend" user input and function results
import admin  # We're testing functions from the admin.py file
