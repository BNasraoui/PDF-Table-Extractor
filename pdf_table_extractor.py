import customtkinter as ctk
import pdfplumber
import pandas as pd
from tkinter import filedialog
import os
import re

# Define the fixed column headers
FIXED_COLUMNS = [
    'PERIOD',
    'PROPERTIES SOLD',
    'MEDIAN VALUE',
    'GROWTH',
    'DAYS ON MARKET',
    'LISTINGS',
    'ASKING RENT'
]

class TableExtractorApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("PDF Table Extractor")
        self.window.geometry("800x600")
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(
            self.window,
            text="PDF Table Extractor",
            font=("Arial", 24)
        )
        title.grid(row=0, column=0, pady=20, padx=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            self.window,
            text="Select a PDF file to extract the table from page 4",
            font=("Arial", 16)
        )
        instructions.grid(row=1, column=0, pady=10, padx=20)
        
        # Button Frame
        button_frame = ctk.CTkFrame(self.window)
        button_frame.grid(row=2, column=0, pady=10, padx=20)
        
        # Select File Button
        self.select_button = ctk.CTkButton(
            button_frame,
            text="Select PDF File",
            command=self.select_file
        )
        self.select_button.pack(side="left", padx=10)
        
        # Preview Button
        self.preview_button = ctk.CTkButton(
            button_frame,
            text="Preview Table",
            command=self.preview_table,
            state="disabled"
        )
        self.preview_button.pack(side="left", padx=10)
        
        # Status Text
        self.status_text = ctk.CTkTextbox(
            self.window,
            height=200,
            width=700
        )
        self.status_text.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")
        
        self.current_file = None
        self.current_table = None
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.current_file = file_path
            self.status_text.delete("1.0", "end")
            self.status_text.insert("1.0", f"Processing {os.path.basename(file_path)}...\n")
            self.extract_table(file_path)
    
    def preview_table(self):
        if self.current_table is not None:
            preview = self.current_table.head(10).to_string()
            self.status_text.delete("1.0", "end")
            self.status_text.insert("1.0", "Table Preview (first 10 rows):\n\n")
            self.status_text.insert("end", preview)
            self.status_text.insert("end", "\n\nNote: This is just a preview. The full table will be saved to CSV.")
    
    def extract_table(self, pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if len(pdf.pages) < 4:
                    self.status_text.insert("end", "Error: PDF has less than 4 pages\n")
                    return
                
                page = pdf.pages[3]  # 0-based index, so page 4 is index 3
                
                # Get all text from the page
                text = page.extract_text()
                
                # Get all words with their positions
                words = page.extract_words()
                
                # Print the extracted words for debugging
                self.status_text.insert("end", f"Found {len(words)} words on page 4\n")
                
                # Sort words by y-position (vertical position)
                words_by_line = {}
                for word in words:
                    # Round the y-position to group words in the same line
                    y_pos = round(word['top'])
                    if y_pos not in words_by_line:
                        words_by_line[y_pos] = []
                    words_by_line[y_pos].append(word)
                
                # Sort each line's words by x-position (horizontal position)
                for y_pos in words_by_line:
                    words_by_line[y_pos] = sorted(words_by_line[y_pos], key=lambda w: w['x0'])
                
                # Get the text of each line
                lines = []
                for y_pos in sorted(words_by_line.keys()):
                    line_text = ' '.join(word['text'] for word in words_by_line[y_pos])
                    lines.append(line_text)
                
                # Print the lines for debugging
                self.status_text.insert("end", f"Found {len(lines)} lines of text\n")
                for i, line in enumerate(lines[:10]):  # Show first 10 lines
                    self.status_text.insert("end", f"Line {i}: {line}\n")
                
                # Find the table data
                data_rows = []
                in_table = False
                table_start_patterns = ['PERIOD', 'PROPERTIES SOLD', 'MEDIAN VALUE']
                
                for i, line in enumerate(lines):
                    # Check if this line contains table headers
                    if any(pattern in line for pattern in table_start_patterns):
                        in_table = True
                        continue
                    
                    # If we're in the table section, extract data rows
                    if in_table:
                        # Check if this line looks like a data row (has year/quarter pattern and numbers)
                        # Look for patterns like "Q1 2020" or "2020" and at least 2-3 numbers
                        year_pattern = re.search(r'(Q[1-4]\s*\d{4}|\d{4})', line)
                        number_count = len(re.findall(r'\$?\d[\d,]*(\.\d+)?%?', line))
                        
                        if year_pattern and number_count >= 2:
                            # This line likely contains table data
                            self.status_text.insert("end", f"Found data row: {line}\n")
                            
                            # Simply replace spaces with commas
                            comma_line = line.replace(' ', ',')
                            
                            # Split into parts by comma
                            parts = comma_line.split(',')
                            
                            # Ensure we have the right number of columns
                            while len(parts) < len(FIXED_COLUMNS):
                                parts.append('')
                            
                            # Only take the first N columns we need
                            parts = parts[:len(FIXED_COLUMNS)]
                            
                            data_rows.append(parts)
                
                if not data_rows:
                    # Fallback: just look for lines with multiple numbers
                    self.status_text.insert("end", "No structured data found, looking for lines with multiple numbers...\n")
                    
                    for line in lines:
                        # Skip header-like lines
                        if any(header in line for header in ['PERIOD', 'PROPERTIES', 'MEDIAN']):
                            continue
                        
                        # Look for lines with multiple numbers (including negatives)
                        numbers = re.findall(r'-?\$?\d[\d,]*(\.\d+)?%?', line)
                        if len(numbers) >= 3:
                            # Try to split the line sensibly
                            parts = re.split(r'\s{2,}', line)  # Split by 2+ spaces
                            
                            # Handle dash symbols as empty values
                            parts = ['' if part.strip() == '-' else part for part in parts]
                            
                            # Make sure negative signs are preserved
                            for i, part in enumerate(parts):
                                # If part starts with negative sign but is separated by space
                                if i > 0 and parts[i-1].strip() == '-' and re.match(r'\d', part):
                                    parts[i] = '-' + part
                                    parts[i-1] = ''
                            
                            # Remove empty parts
                            parts = [p for p in parts if p.strip()]
                            
                            if len(parts) >= 3:
                                # Make sure we have the right number of columns
                                while len(parts) < len(FIXED_COLUMNS):
                                    parts.append('')
                                if len(parts) > len(FIXED_COLUMNS):
                                    parts = parts[:len(FIXED_COLUMNS)]
                                
                                data_rows.append(parts)
                
                if not data_rows:
                    self.status_text.insert("end", "No data rows found in the document\n")
                    return
                
                # Create DataFrame with fixed column headers
                df = pd.DataFrame(data_rows, columns=FIXED_COLUMNS)
                
                # Replace spaces with commas in all cells
                for column in df.columns:
                    df[column] = df[column].apply(lambda x: str(x).replace(' ', ',') if pd.notna(x) else x)
                
                self.current_table = df
                
                # Save to CSV
                output_path = pdf_path.rsplit('.', 1)[0] + '_extracted_table.csv'
                df.to_csv(output_path, index=False)
                
                self.status_text.insert("end", f"Success! Saved {len(df)} rows to CSV:\n{output_path}\n")
                self.preview_button.configure(state="normal")
        
        except Exception as e:
            self.status_text.insert("end", f"Error: {str(e)}\n")
            import traceback
            self.status_text.insert("end", traceback.format_exc())
            self.preview_button.configure(state="disabled")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TableExtractorApp()
    app.run() 