#!/usr/bin/env python3
"""
Community E-Library System - Test Script
Simple unit tests for student and admin functionality
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from storage import ELibrary, User, Resource
from student import StudentInterface
from admin import AdminInterface
from cli import CLIHelper


class TestELibrary(unittest.TestCase):
    """Test cases for ELibrary core functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Initialize library with test data file
        self.library = ELibrary()
        self.library.data_file = 'test_library_data.json'
        
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_user_registration_and_login(self):
        """Test user registration and login functionality"""
        # Test successful registration
        result = self.library.register_user("testuser", "testpass", "test@email.com")
        self.assertTrue(result)
        self.assertIn("testuser", self.library.users)
        
        # Test duplicate registration
        result = self.library.register_user("testuser", "newpass", "new@email.com")
        self.assertFalse(result)
        
        # Test successful login
        login_result = self.library.login("testuser", "testpass")
        self.assertTrue(login_result)
        self.assertEqual(self.library.current_user.username, "testuser")
        
        # Test failed login
        self.library.logout()
        login_result = self.library.login("testuser", "wrongpass")
        self.assertFalse(login_result)
        self.assertIsNone(self.library.current_user)
    
    def test_add_resource(self):
        """Test adding resources to the library"""
        resource_id = self.library.add_resource(
            title="Test Book",
            author="Test Author",
            subject="Testing",
            language="English",
            file_path="/test/path.pdf",
            category="Core Subjects",
            description="A test book"
        )
        
        self.assertIn(resource_id, self.library.resources)
        resource = self.library.resources[resource_id]
        self.assertEqual(resource.title, "Test Book")
        self.assertEqual(resource.author, "Test Author")
        self.assertEqual(resource.download_count, 0)
        self.assertEqual(resource.view_count, 0)
    
    def test_search_resources(self):
        """Test resource search functionality"""
        # Add test resources
        self.library.add_resource("Python Programming", "John Doe", "Programming", "English", "/path1.pdf")
        self.library.add_resource("Java Basics", "Jane Smith", "Programming", "English", "/path2.pdf")
        self.library.add_resource("History of Rwanda", "Bob Johnson", "History", "Kinyarwanda", "/path3.pdf")
        
        # Test search by title
        results = self.library.search_resources("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Programming")
        
        # Test search by author
        results = self.library.search_resources("Jane")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Jane Smith")
        
        # Test search by subject
        results = self.library.search_resources("Programming")
        self.assertEqual(len(results), 2)
        
        # Test search with no results
        results = self.library.search_resources("Nonexistent")
        self.assertEqual(len(results), 0)
    
    def test_favorites_functionality(self):
        """Test favorites functionality"""
        # Create user and resource
        self.library.register_user("testuser", "testpass")
        self.library.login("testuser", "testpass")
        resource_id = self.library.add_resource("Favorite Book", "Author", "Subject", "English", "/path.pdf")
        
        # Test adding to favorites
        result = self.library.add_to_favorites(resource_id)
        self.assertTrue(result)
        self.assertIn(resource_id, self.library.current_user.favorites)
        
        # Test adding duplicate favorite
        result = self.library.add_to_favorites(resource_id)
        self.assertFalse(result)
        
        # Test getting favorites
        favorites = self.library.get_user_favorites()
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites[0].title, "Favorite Book")
    
    def test_resource_categories(self):
        """Test resource categorization"""
        # Add resources to different categories
        id1 = self.library.add_resource("Book 1", "Author 1", "Subject", "English", "/path1.pdf", "Core Subjects")
        id2 = self.library.add_resource("Book 2", "Author 2", "Subject", "English", "/path2.pdf", "Local Storybooks")
        id3 = self.library.add_resource("Book 3", "Author 3", "Subject", "English", "/path3.pdf", "Core Subjects")
        
        # Test getting resources by category
        core_resources = self.library.get_resources_by_category("Core Subjects")
        self.assertEqual(len(core_resources), 2)
        
        story_resources = self.library.get_resources_by_category("Local Storybooks")
        self.assertEqual(len(story_resources), 1)
        
        empty_category = self.library.get_resources_by_category("Study Skills")
        self.assertEqual(len(empty_category), 0)


class TestStudentInterface(unittest.TestCase):
    """Test cases for StudentInterface"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        self.library = ELibrary()
        self.library.data_file = 'test_library_data.json'
        self.cli_helper = CLIHelper()
        self.student_interface = StudentInterface(self.library, self.cli_helper)
        
        # Add test data
        self.library.add_resource("Test Book", "Test Author", "Testing", "English", "/test.pdf")
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_student_registration(self, mock_print, mock_input):
        """Test student registration process"""
        # Use a list that cycles for unlimited "Press Enter" prompts
        inputs = ['newuser', 'password123', 'user@test.com']
        mock_input.side_effect = inputs + [''] * 10  # Add many empty strings for "Press Enter"
        
        result = self.student_interface.student_registration()
        self.assertTrue(result)
        self.assertIn('newuser', self.library.users)
        self.assertEqual(self.library.current_user.username, 'newuser')
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_student_login_success(self, mock_print, mock_input):
        """Test successful student login"""
        # First register a user
        self.library.register_user('testuser', 'testpass')
        
        # Provide inputs plus many empty strings for "Press Enter" prompts
        inputs = ['testuser', 'testpass']
        mock_input.side_effect = inputs + [''] * 10
        
        result = self.student_interface.student_login()
        self.assertTrue(result)
        self.assertEqual(self.library.current_user.username, 'testuser')
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_student_login_failure(self, mock_print, mock_input):
        """Test failed student login"""
        # Provide inputs plus many empty strings for "Press Enter" prompts
        inputs = ['wronguser', 'wrongpass']
        mock_input.side_effect = inputs + [''] * 10
        
        result = self.student_interface.student_login()
        self.assertFalse(result)
        self.assertIsNone(self.library.current_user)


class TestAdminInterface(unittest.TestCase):
    """Test cases for AdminInterface"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        self.library = ELibrary()
        self.library.data_file = 'test_library_data.json'
        self.cli_helper = CLIHelper()
        self.admin_interface = AdminInterface(self.library, self.cli_helper)
        
        # Login as admin for tests
        self.library.login('admin', 'admin123')
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_add_new_resource(self, mock_print, mock_input):
        """Test adding new resource through admin interface"""
        mock_input.side_effect = [
            'New Test Book',        # title
            'Admin Author',         # author
            'Admin Testing',        # subject
            'English',             # language
            '/admin/test.pdf',     # file path
            'Test description',    # description
            '1',                   # category choice (Core Subjects)
            ''                     # Press Enter to continue
        ]
        
        initial_count = len(self.library.resources)
        self.admin_interface.add_new_resource()
        
        # Check if resource was added
        self.assertEqual(len(self.library.resources), initial_count + 1)
        
        # Find the added resource
        added_resource = None
        for resource in self.library.resources.values():
            if resource.title == 'New Test Book':
                added_resource = resource
                break
        
        self.assertIsNotNone(added_resource)
        self.assertEqual(added_resource.author, 'Admin Author')
        self.assertEqual(added_resource.category, 'Core Subjects')
    
    def test_usage_report_generation(self):
        """Test usage report generation"""
        # Add some test resources with usage data
        resource1_id = self.library.add_resource("Popular Book", "Author1", "Subject", "English", "/path1.pdf")
        resource2_id = self.library.add_resource("Less Popular", "Author2", "Subject", "English", "/path2.pdf")
        
        # Simulate some usage
        self.library.resources[resource1_id].download_count = 10
        self.library.resources[resource1_id].view_count = 15
        self.library.resources[resource2_id].download_count = 3
        self.library.resources[resource2_id].view_count = 5
        
        # Add some test users
        self.library.register_user("student1", "pass1")
        self.library.register_user("student2", "pass2")
        
        report = self.library.get_usage_report()
        
        self.assertEqual(report['total_resources'], 2)
        self.assertEqual(report['total_users'], 2)  # Only students counted
        self.assertEqual(len(report['most_downloaded']), 2)
        self.assertEqual(len(report['most_viewed']), 2)
        
        # Check ordering (most downloaded first)
        self.assertEqual(report['most_downloaded'][0].title, "Popular Book")
        self.assertEqual(report['most_viewed'][0].title, "Popular Book")


class TestResourceOperations(unittest.TestCase):
    """Test resource-specific operations"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        self.library = ELibrary()
        self.library.data_file = 'test_library_data.json'
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_view_resource_increments_count(self):
        """Test that viewing a resource increments view count"""
        resource_id = self.library.add_resource("View Test", "Author", "Subject", "English", "/nonexistent.pdf")
        
        initial_view_count = self.library.resources[resource_id].view_count
        
        # Mock the file operations to avoid actual file opening
        with patch.object(self.library, '_open_file') as mock_open:
            result = self.library.view_resource(resource_id)
            
            # Check that view count was incremented
            self.assertEqual(
                self.library.resources[resource_id].view_count, 
                initial_view_count + 1
            )
    
    def test_download_resource_increments_count(self):
        """Test that downloading a resource increments download count"""
        resource_id = self.library.add_resource("Download Test", "Author", "Subject", "English", "/nonexistent.pdf")
        
        initial_download_count = self.library.resources[resource_id].download_count
        
        result = self.library.download_resource(resource_id)
        
        # Check that download count was incremented
        self.assertEqual(
            self.library.resources[resource_id].download_count, 
            initial_download_count + 1
        )


def run_tests():
    """Function to run all tests"""
    print("Running Community E-Library System Tests...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestELibrary,
        TestStudentInterface, 
        TestAdminInterface,
        TestResourceOperations
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print detailed error information
    if result.errors:
        print("\n" + "=" * 50)
        print("ERRORS:")
        for test, error in result.errors:
            print(f"\n{test}:")
            print(error)
    
    if result.failures:
        print("\n" + "=" * 50)
        print("FAILURES:")
        for test, failure in result.failures:
            print(f"\n{test}:")
            print(failure)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("All tests passed! ✅")
    else:
        print("Some tests failed! ❌")
        
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
