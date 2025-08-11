"""
RePKG UI - Application Constants
===============================

Contains all application constants, default values, and configuration definitions.
"""

# Application Information
APP_NAME = "RePKG UI"
APP_TITLE = "RePKG UI - by tmk301"
APP_VERSION = "2.0.0"
APP_AUTHOR = "tmk301"
APP_REPO = "https://github.com/tmk301"
ORIGINAL_REPO = "https://github.com/notscuffed/repkg"

# Window Configuration
WINDOW_GEOMETRY = "900x700"
WINDOW_THEME = "darkly"  # Default theme
ABOUT_WINDOW_GEOMETRY = "350x200"

# Theme Configuration
THEMES = {
    "dark": "darkly",
    "light": "flatly"
}
THEME_ICONS = {
    "dark": "🌙",
    "light": "☀️"
}

# File Configuration
CONFIG_FILE = "config.ini"
LOG_FILE = "logs.txt"
ICON_FILE = "icon.ico"
REPKG_EXE = "RePKG.exe"

# UI Configuration
AUTO_SAVE_DELAY = 500  # milliseconds
CONSOLE_OUTPUT_HEIGHT = 20

# Default Configuration Values
DEFAULT_CONFIG = {
    # General settings
    "log": "true",
    "mode": "extract",
    "input": "",
    "output": "",
    "theme": "dark",  # Default to dark theme
    
    # Extraction options
    "tex": "false",
    "singledir": "false", 
    "usename": "false",
    "no_tex_convert": "false",
    "overwrite": "false",
    "copyproject": "false",
    "exts_only": "",
    "exts_ignore": "",
    
    # Info mode options
    "sortby": "name",
    "sort": "true",
    "printentries": "true",
    "info_tex": "false",
    "projectinfo": "",
    "title_filter": ""
}

# UI Colors
LINK_COLOR = "#4A9EFF"
LINK_HOVER_COLOR = "#66B3FF"
LINK_PRESSED_COLOR = "#2E86FF"

# Extract Mode Options
EXTRACT_OPTIONS = [
    ("tex", "Convert all TEX files into images from specified directory in input"),
    ("singledir", "Should all extracted files be put in one directory instead of their entry path"),
    ("usename", "Use name from project.json as project subfolder name instead of id"),
    ("no_tex_convert", "Don't convert TEX files into images while extracting PKG"),
    ("overwrite", "Overwrite all existing files"),
    ("copyproject", "Copy project.json and preview.jpg from beside PKG into output directory")
]

# Info Mode Options
INFO_OPTIONS = [
    ("sort", "Sort entries ascending"),
    ("printentries", "Print entries in packages"),
    ("info_tex", "Dump info about all TEX files from specified directory")
]

# Sorting Options
SORT_OPTIONS = ["name", "extension", "size"]

# File Types
FILE_TYPES = [("PKG/TEX files", "*.pkg *.tex"), ("All files", "*.*")]
