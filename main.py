#!/usr/bin/env python3
"""
RePKG UI - Modular Version
=========================

Modern, modular graphical interface for the RePKG command-line tool.

This is the refactored version with improved architecture:
- Separated concerns: UI, business logic, configuration
- Modular structure for better maintainability
- Professional code organization
- Easy testing and extensibility

Author: tmk301 (https://github.com/tmk301)
Based on: RePKG by notscuffed (https://github.com/notscuffed/repkg)
License: MIT License
"""

from repkg_ui import MainWindow


def main():
    """Main application entry point."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
