# RePKG-UI

A modern, modular graphical interface for the [RePKG](https://github.com/notscuffed/repkg) command-line tool.

## Overview

RePKG-UI provides an intuitive GUI wrapper for the powerful RePKG tool, making it easier to extract and manipulate UE4/UE5 pak files. This refactored version features improved architecture with separated concerns, modular structure, and professional code organization.

## Features

- **Modern GUI Interface** - Clean and user-friendly interface built with Python
- **Modular Architecture** - Well-organized codebase with separated UI and business logic
- **Configuration Management** - Easy-to-use configuration system
- **File Utilities** - Built-in file handling and management tools
- **RePKG Integration** - Seamless integration with the RePKG command-line tool

## Project Structure

```
RePKG-UI/
├── main.py                 # Application entry point
├── config.ini             # Configuration file
├── RePKG_UI.exe           # Compiled executable
├── repkg_ui/              # Main package
│   ├── __init__.py
│   ├── constants.py       # Application constants
│   ├── core/              # Core business logic
│   │   ├── config.py      # Configuration management
│   │   ├── file_utils.py  # File handling utilities
│   │   └── repkg_runner.py # RePKG integration
│   └── ui/                # User interface components
│       ├── dialogs.py     # Dialog windows
│       ├── main_window.py # Main application window
│       └── styles.py      # UI styling
└── README.md
```

## Requirements
Required for build, not for use. If you are not a developer, just don't care about this section.
- Python 3.7+
- [RePKG.exe](https://github.com/notscuffed/repkg)
- Required Python packages (see installation)

## Installation

### Option 1: Use Pre-built Executable
1. Download `RePKG_UI.exe` from the releases
2. Run the executable

### Option 2: Run from Source
1. Clone this repository:
   ```bash
   git clone https://github.com/tmk301/RePKG-UI.git
   cd RePKG-UI
   ```

2. Install required dependencies:
   Run `setup_and_test.bat` 
   or:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Launch the Application**
   - Run `RePKG_UI.exe` or `python main.py`

2. **Run**
   - Select tex/pkg file or folder
   - Choose extraction options
   - Click Run to process

## Configuration

The application uses a `config.ini` file to store settings. This file is automatically created on first run and includes:

- Default extraction directory
- UI preferences
- Other application settings

## Development

### Architecture

The project follows a modular architecture:

- **`repkg_ui/core/`** - Business logic and core functionality
- **`repkg_ui/ui/`** - User interface components and styling
- **`repkg_ui/constants.py`** - Application-wide constants
- **`main.py`** - Application entry point and initialization

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Building Executable

To build the executable using the built-in tool:

Run `setup_and_test.bat`

Or using .spec file:

```bash
pyinstaller build.spec
```

## Credits

- **Author**: [tmk301](https://github.com/tmk301)
- **Based on**: [RePKG](https://github.com/notscuffed/repkg) by [notscuffed](https://github.com/notscuffed)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page for existing solutions
2. Create a new issue with detailed information about your problem
3. Include your system information and steps to reproduce

## Acknowledgments

- Thanks to [notscuffed](https://github.com/notscuffed) for the original RePKG tool