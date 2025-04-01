"""
Setup script for creating a macOS app using PyInstaller
"""

import os
import sys
from setuptools import setup

APP_NAME = "PDF Table Extractor"
APP_SCRIPT = "pdf_table_extractor.py"

if __name__ == "__main__":
    setup(
        name=APP_NAME,
        version="1.0",
        description="Extract tables from PDF documents",
        author="Your Name",
        author_email="your.email@example.com",
    ) 