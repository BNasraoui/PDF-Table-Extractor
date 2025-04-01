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
pip install pyinstaller

# Install additional PyInstaller dependencies
echo "Installing PyInstaller utilities..."
pip install pillow

# Build the app using PyInstaller with our spec file
echo "Building macOS app..."
pyinstaller app.spec

# Make the app file executable
echo "Making app executable..."
chmod +x "dist/PDF Table Extractor.app/Contents/MacOS/PDF Table Extractor"

# Copy the app to a more accessible location
echo "Finalizing..."
cp -r "dist/PDF Table Extractor.app" .

# Create a zip file for easy distribution
echo "Creating zip archive for distribution..."
zip -r "PDF_Table_Extractor.zip" "PDF Table Extractor.app"

# Deactivate the virtual environment
deactivate

# Clean up build files (but keep the dist directory)
rm -rf build_env build

echo "Done! The app has been created as 'PDF Table Extractor.app'"
echo "A zip file 'PDF_Table_Extractor.zip' has also been created for easy sharing"
echo "You can now drag and drop the app file to your Applications folder or share the zip file." 