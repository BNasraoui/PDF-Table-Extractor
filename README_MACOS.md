# PDF Table Extractor for macOS

## Using the Application

### Option 1: Use the pre-built application (recommended)

1. Download the `PDF Table Extractor.app` file
2. Double-click to run it
   - If you see a security warning, go to System Preferences > Security & Privacy and click "Open Anyway"
3. Click "Select PDF File" to choose your PDF document
4. The application will automatically extract the table from page 4
5. A CSV file will be created in the same folder as your PDF

### Option 2: Building the application yourself

If you didn't receive the pre-built application, you can build it yourself:

1. Make sure you have Python installed (comes with macOS)
2. Open Terminal (in Applications > Utilities)
3. Navigate to this folder using `cd /path/to/this/folder`
4. Run the build script: `sh build_macos_app.sh`
5. Once built, you'll find the application in the same folder

## Troubleshooting

If you encounter any issues:

- Make sure your PDF document has at least 4 pages
- Make sure there is a table on page 4
- Check that the table has the expected column structure
- If you see "operation not permitted" errors, try moving the app to your Applications folder

## About This Tool

This tool automatically extracts table data from page 4 of PDF documents. It uses the following column headers:

- PERIOD
- PROPERTIES SOLD
- MEDIAN VALUE
- GROWTH
- DAYS ON MARKET
- LISTINGS
- ASKING RENT

The extracted data is saved as a CSV file that can be opened in Excel, Numbers, or any spreadsheet application. 