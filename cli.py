#!/usr/bin/env python3
"""
Community E-Library System - Command Line Interface
Contains the main CLI functionality and interface coordination
"""

import os
from storage import ELibrary
from student import StudentInterface
from admin import AdminInterface

class CLIHelper:
    """Helper class for CLI operations"""
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title: str):
        """Display a formatted header"""
        print("\n" + "="*50)
        print(f"  {title}")
        print("="*50)
    
    def get_input(self, prompt: str, input_type=str):
        """Get user input with type conversion"""
        while True:
            try:
                value = input(prompt)
                if input_type == int:
                    return int(value)
                return value
            except ValueError:
                print("Invalid input. Please try again.")

class ELibraryInterface:
    """Main interface class that coordinates all CLI operations"""
    
    def __init__(self):
        self.library = ELibrary()
        self.cli_helper = CLIHelper()
        self.student_interface = StudentInterface(self.library, self.cli_helper)
        self.admin_interface = AdminInterface(self.library, self.cli_helper)
    
    def start(self):
        """Main entry point"""
        while True:
            self.cli_helper.clear_screen()
            self.cli_helper.display_header("Welcome to the Community E-Library")
            print("\nAre you a:")
            print("1. Student")
            print("2. Admin")
            print("3. Exit")
            
            choice = self.cli_helper.get_input("\nEnter your choice: ", int)
            
            if choice == 1:
                self.student_interface.student_interface()
            elif choice == 2:
                self.admin_interface.admin_interface()
            elif choice == 3:
                print("Thank you for using Community E-Library!")
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")