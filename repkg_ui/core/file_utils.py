"""
RePKG UI - File Utilities
=========================

Utilities for file operations, resource path handling, and file dialogs.
"""

import os
import sys
from tkinter import filedialog
from ..constants import FILE_TYPES, ICON_FILE, REPKG_EXE


def get_resource_path(filename):
    """
    Determine the correct path for resources when running as executable or script.
    
    Args:
        filename (str): Name of the resource file
        
    Returns:
        str: Absolute path to the resource file
    """
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller executable
        return os.path.join(sys._MEIPASS, filename)
    # Running as Python script
    return os.path.join(os.path.abspath("."), filename)


def get_repkg_executable_path():
    """Get the path to the RePKG executable."""
    return get_resource_path(REPKG_EXE)


def get_icon_path():
    """Get the path to the application icon."""
    return get_resource_path(ICON_FILE)


def select_pkg_file():
    """Open file dialog to select PKG or TEX files for input."""
    return filedialog.askopenfilename(
        title="Select a PKG or TEX file",
        filetypes=FILE_TYPES
    )


def select_input_folder():
    """Open folder dialog to select directory for input."""
    return filedialog.askdirectory(title="Select a folder")


def select_output_folder():
    """Open folder dialog to select output directory."""
    return filedialog.askdirectory(title="Select output directory")
