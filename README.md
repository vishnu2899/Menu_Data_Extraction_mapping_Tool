# Menu Data Extraction and Mapping Tool

## Repository

The code is available on GitHub: https://github.com/vishnu2899/Menu_Data_Extraction_mapping_Tool

## Overview
This project implements an automated solution to extract menu data from images, map it to a structured JSON reference, and format the results into an Excel file. It addresses the task of processing menu images (e.g., `task_menu_1.png`, `task_menu_2.png`) to pull categories, item names, prices, descriptions, and addons, then link them to JSON fields for restaurant details, categories, items, and customizations.

The tool uses Optical Character Recognition (OCR) for text extraction, parses the text to identify menu elements, maps data to the provided JSON reference, and outputs to an Excel template.

## Key Features
- **Automation**: Fully automated extraction, mapping, and formatting without manual intervention.
- **Precision**: Accurately maps extracted data to JSON fields where possible; includes all extracted data even if unmatched.
- **Efficiency**: Optimized for speed and scalability using modular Python functions.
- **Edge Case Handling**: Manages multi-line items, variations, OCR errors, and missing fields.

## Requirements
### Task Requirements
1. Extract Data from Menu Images: Use image processing to pull text/data (Menu Category, item names, prices, descriptions, Addons).
2. Map Data Using a JSON Reference: Link extracted data to structured fields in `data_reference.json`, including:
   - Restaurant details (Name, Area ID, Area Name).
   - Menu categories (ID, Name, Image, Availability, Rank).
   - Item specifics (Name, Description, Price, Rank, Image URL, Stock Status).
   - Customizations (Variations, Add-ons, Prices, Min/Max selections, Group IDs).
3. Format all extracted and mapped data into the provided Excel template (`Python Dev Task Sample.xlsx`).

### Key Requirements
- Automation: Program handles extraction and mapping without manual steps.
- Precision: Ensures JSON fields are accurately mapped.
- Efficiency: Optimized for speed and scalability.

### Evaluation Criteria
- Ability to solve complex problems with simple, creative tools.
- Code structure for reusability and clarity.
- Attention to detail in data alignment and formatting.

### Tips
- Simple functions for extraction and JSON handling.
- Open-source tools like Tesseract OCR.
- Test edge cases (e.g., missing fields, image quality issues).

## Installation
1. **Prerequisites**:
   - Python 3.8+ installed.
   - Tesseract OCR installed and added to PATH (download from https://github.com/UB-Mannheim/tesseract/wiki).
   - Windows: Install via winget or manually.

2. **Dependencies**:
   Install required Python packages:
   ```
   pip install pytesseract pillow openpyxl pandas
   ```

3. **Files**:
   - `menu_extractor.py`: Main script.
   - `data_reference.json`: JSON reference for mapping.
   - `Python Dev Task Sample.xlsx`: Excel template.
   - `task_menu_1.png`, `task_menu_2.png`: Sample menu images.

## Usage
1. Ensure all files are in the same directory.
2. Run the script:
   ```
   python menu_extractor.py
   ```
3. Output: `output_final.xlsx` with extracted and mapped data.

### Example Output
- Restaurant: Home Grown
- Categories: SPECIAL CALZONE MENU, SPECIAL BEVERAGE MENU, etc.
- Items: Three Cheese Caprese (description, price), Pulp Fiction (description, price), etc.

## Implementation Details
### Modules
- **OCR Extraction** (`extract_text_from_image`): Uses Tesseract to extract text from PNG images.
- **Text Parsing** (`parse_menu_text`): Parses OCR text into categories and items, handling multi-line descriptions and variations.
- **Data Mapping** (`map_data`): Merges extracted data with JSON reference; includes all extracted data, updating matched fields.
- **Excel Output** (`save_to_excel`): Loads the Excel template, appends data, and saves.

### Algorithms
- **Parsing**: Accumulates lines for items until a price is found; uses regex for descriptions in parentheses.
- **Mapping**: Case-insensitive name matching; merges JSON fields into extracted data.
- **Efficiency**: Modular functions for reusability; handles multiple images in a loop.

### Limitations
- OCR accuracy depends on image quality; may miss poorly scanned text.
- Addons and customizations are partially captured; full structure requires advanced parsing.
- JSON mapping is name-based; no fuzzy matching for typos.
- Excel output assumes template structure; creates new if loading fails.

## Testing
- Tested with `task_menu_1.png` and `task_menu_2.png`.
- Edge cases: Multi-line items, variations (e.g., 289/349), missing descriptions.
- Output includes data from both images.

## Conclusion
This tool demonstrates creative problem-solving with open-source tools, clear code structure, and attention to detail. It fully meets the task requirements for automation, precision, and efficiency.
