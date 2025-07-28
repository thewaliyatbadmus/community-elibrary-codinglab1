#!/usr/bin/env python3
"""
Community E-Library System - Main Entry Point
A digital library platform for underserved communities
"""

from cli import ELibraryInterface

def main():
    """Main function to run the application"""
    app = ELibraryInterface()
    app.start()

if __name__ == "__main__":
    main()