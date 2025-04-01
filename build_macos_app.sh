#!/bin/bash

# Exit on error
set -e

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv build_env

# Activate the virtual environment
echo "Activating virtual environment..."
source build_env/bin/activate

# Install required packages
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller pillow

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.py[cod] __pycache__ tk_fix.py

# Build the app using PyInstaller with spec file
echo "Building macOS app..."
pyinstaller app.spec

# Make the app file executable
echo "Making app executable..."
chmod +x "dist/PDF Table Extractor.app/Contents/MacOS/PDF Table Extractor"

# Create a zip file for easy distribution
echo "Creating zip archive for distribution..."
cd dist
zip -r "../PDF_Table_Extractor.zip" "PDF Table Extractor.app"
cd ..

# Deactivate the virtual environment
deactivate

echo "Done! The app has been created as 'dist/PDF Table Extractor.app'"
echo "A zip file 'PDF_Table_Extractor.zip' has also been created for easy sharing." 