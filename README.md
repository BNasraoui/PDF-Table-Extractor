# PDF Table Extractor

A simple application that extracts tables from page 4 of PDF documents and saves them as CSV files.

## Download

**Mac Users**: 
1. Go to the [Releases](../../releases) page
2. Download the latest `PDF_Table_Extractor.zip` file
3. Follow the instructions in the INSTALLATION_GUIDE.md file

## Features

- Simple, user-friendly interface
- Automatically extracts tables from page 4 of PDF documents
- Saves extracted data as CSV files that can be opened in Excel or Numbers
- No programming knowledge required

## Usage

1. Launch the application
2. Click "Select PDF File" and choose your PDF document
3. The application automatically extracts the table
4. A CSV file is created in the same folder as your PDF

## Column Structure

The application extracts tables with the following column structure:

- PERIOD
- PROPERTIES SOLD
- MEDIAN VALUE
- GROWTH
- DAYS ON MARKET
- LISTINGS
- ASKING RENT

## For Developers

If you want to modify or build the app yourself:

### Requirements
- Python 3.7+
- Required packages: customtkinter, pdfplumber, pandas

### Setup
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python pdf_table_extractor.py`

### Building the App
- macOS: Run `sh build_macos_app.sh` to create a standalone macOS application