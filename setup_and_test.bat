@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo   RePKG-UI Setup and Testing Script
echo ==========================================
echo.

:menu
echo Please choose an option:
echo [1] Test dependencies and files
echo [2] Install missing dependencies  
echo [3] Test and auto-install if needed
echo [4] Build executable
echo [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto :test_only
if "%choice%"=="2" goto :install_only
if "%choice%"=="3" goto :test_and_install
if "%choice%"=="4" goto :build
if "%choice%"=="5" goto :end
echo Invalid choice. Please try again.
echo.
goto :menu

:test_only
echo.
echo ==========================================
echo Testing RePKG-UI Dependencies and Files
echo ==========================================
call :check_dependencies
call :check_files
echo.
echo [SUCCESS] Testing completed.
pause
goto :menu

:install_only
echo.
echo ==========================================
echo Installing RePKG-UI Dependencies
echo ==========================================
call :install_dependencies
pause
goto :menu

:test_and_install
echo.
echo ==========================================
echo Testing and Auto-Installing Dependencies
echo ==========================================
call :check_dependencies
if !deps_missing! equ 1 (
    echo.
    echo Some dependencies are missing. Installing now...
    call :install_dependencies
) else (
    echo.
    echo All dependencies are already installed!
)
call :check_files
echo.
echo [SUCCESS] Setup completed.
pause
goto :menu

:build
echo.
echo ==========================================
echo Building RePKG-UI Executable
echo ==========================================
call :check_dependencies
call :check_files
if !deps_missing! equ 1 (
    echo [ERROR] Cannot build: Missing dependencies. Please install them first.
    pause
    goto :menu
)
if !files_missing! equ 1 (
    echo [ERROR] Cannot build: Missing required files.
    pause
    goto :menu
)

echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "RePKG_UI.exe" del "RePKG_UI.exe"

echo.
echo Building single-file portable executable...
echo This may take a few minutes...
if exist "build.spec" (
    echo Using existing build.spec file...
    pyinstaller build.spec --clean --noconfirm
) else if exist "repkg_ui.spec" (
    echo Using repkg_ui.spec file...
    pyinstaller repkg_ui.spec --clean --noconfirm
) else (
    echo Creating new spec and building...
    pyinstaller --onefile --windowed --icon=icon.ico --name=RePKG_UI main.py --clean --noconfirm
)

echo.
echo Checking if build was successful...
if exist "dist\RePKG_UI.exe" (
    echo.
    echo [SUCCESS] Build successful!
    echo Moving executable to main directory...
    move "dist\RePKG_UI.exe" "RePKG_UI.exe"
    
    echo.
    echo File Information:
    dir "RePKG_UI.exe" | findstr /C:"RePKG_UI.exe"
    
    echo.
    echo Portable RePKG_UI.exe is ready!
    echo File location: %cd%\RePKG_UI.exe
    echo.
    echo This executable is fully portable and can run on any Windows PC
    echo without requiring Python or any additional installations!
) else (
    echo.
    echo [ERROR] Build failed! Check the error messages above.
    echo Common solutions:
    echo 1. Install missing dependencies: pip install ttkbootstrap
    echo 2. Make sure all files are present in the directory
    echo 3. Check if antivirus is blocking PyInstaller
)

echo.
echo Cleaning up temporary files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

pause
goto :menu

:check_dependencies
echo.
echo Checking Python dependencies...
set deps_missing=0

python -c "import ttkbootstrap; print('ttkbootstrap installed')" 2>nul || (
    echo ttkbootstrap not installed
    set deps_missing=1
)

python -c "import PIL; print('Pillow installed')" 2>nul || (
    echo Pillow not installed
    set deps_missing=1
)

python -c "import tkinter; print('tkinter available')" 2>nul || (
    echo tkinter not available
    set deps_missing=1
)

python -c "import configparser; print('configparser available')" 2>nul || (
    echo configparser not available
    set deps_missing=1
)

echo.
echo Checking build tools...
pyinstaller --version 2>nul && echo PyInstaller available || (
    echo PyInstaller not installed
    set deps_missing=1
)

goto :eof

:check_files
echo.
echo Checking required files...
set files_missing=0

if exist "main.py" (echo main.py found) else (
    echo main.py missing
    set files_missing=1
)

if exist "repkg_ui\" (echo repkg_ui package found) else (
    echo repkg_ui package missing
    set files_missing=1
)

if exist "version_info.py" (echo version_info.py found) else (
    echo version_info.py missing - version info will not be included in executable
)

if exist "build.spec" (echo build.spec found) else (
    echo build.spec missing - will use default PyInstaller settings
)

if exist "config.ini" (echo config.ini found) else (
    echo config.ini missing - will be created on first run
)

if exist "icon.ico" (echo icon.ico found) else (
    echo icon.ico missing - default icon will be used
)

if exist "RePKG.exe" (echo RePKG.exe found) else (
    echo RePKG.exe missing - please ensure RePKG tool is available
)

goto :eof

:install_dependencies
echo.
echo Installing required Python packages...

echo.
echo [1/3] Installing ttkbootstrap...
pip install ttkbootstrap
if errorlevel 1 (
    echo [ERROR] Failed to install ttkbootstrap
    goto :install_error
)

echo.
echo [2/3] Installing Pillow...
pip install Pillow
if errorlevel 1 (
    echo [ERROR] Failed to install Pillow
    goto :install_error
)

echo.
echo [3/3] Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    goto :install_error
)

echo.
echo [SUCCESS] All dependencies installed successfully!
echo.
echo You can now:
echo - Run: python main.py (to test the application)
echo - Build: Choose option 4 from menu (to build executable)
set deps_missing=0
goto :eof

:install_error
echo.
echo [ERROR] Installation failed!
echo Please try:
echo - Running as administrator
echo - Checking your internet connection  
echo - Using: pip install --user [package_name]
goto :eof

:end
echo.
echo Thank you for using RePKG-UI setup script!
pause
exit /b 0