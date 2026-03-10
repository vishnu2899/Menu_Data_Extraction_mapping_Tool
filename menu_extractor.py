import json
import pytesseract
from PIL import Image
import openpyxl
import pandas as pd
import os

# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """Extract text from image using OCR."""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

def parse_menu_text(text):
    """Parse the extracted text to identify menu categories, items, prices, etc."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    menu_data = {
        'categories': [],
        'items': []
    }
    current_category = None
    accumulated_item = []
    for line in lines:
        if line.isupper() and len(line) > 2:
            # Likely a category
            current_category = line
            menu_data['categories'].append({'name': line})
        else:
            # Accumulate until we find a price
            accumulated_item.append(line)
            # Check if this line or accumulated has a price (digits)
            full_item = ' '.join(accumulated_item)
            # Find the last part that looks like price
            parts = full_item.split()
            price = None
            name_desc = full_item
            for i in range(len(parts) - 1, -1, -1):
                if parts[i].replace('/', '').replace('-', '').replace('.', '').replace(',', '').isdigit():
                    price = ' '.join(parts[i:])
                    name_desc = ' '.join(parts[:i])
                    break
            if price:
                # Parse name and description
                # Assume description in parentheses
                import re
                match = re.match(r'(.+?)\s*\((.+)\)', name_desc)
                if match:
                    name = match.group(1).strip()
                    description = match.group(2).strip()
                else:
                    name = name_desc
                    description = ''
                # Handle variations if / in price
                if '/' in price:
                    variations = []
                    var_parts = price.split('/')
                    for vp in var_parts:
                        vp = vp.strip()
                        if vp:
                            variations.append({'price': vp})
                    price = None  # Set to None if variations
                else:
                    variations = None
                menu_data['items'].append({
                    'name': name,
                    'price': price,
                    'variations': variations,
                    'category': current_category,
                    'description': description
                })
                accumulated_item = []  # Reset
    return menu_data

def load_json_reference(json_path):
    """Load the JSON reference file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def map_data(extracted_data, json_ref):
    """Map extracted data to JSON reference fields, including all extracted data."""
    mapped = {
        'restaurant': json_ref['restaurants'][0]['details'],
        'areas': json_ref['areas'],
        'categories': [],
        'items': []
    }
    # For categories, include all extracted, merge with JSON if match
    for cat in extracted_data['categories']:
        cat_entry = {'categoryname': cat['name'], 'categoryid': '', 'active': '', 'categoryrank': ''}
        for ref_cat in json_ref['categories']:
            if ref_cat['categoryname'].lower() == cat['name'].lower():
                cat_entry.update(ref_cat)
                break
        mapped['categories'].append(cat_entry)
    # For items, include all extracted, merge with JSON if match
    for item in extracted_data['items']:
        item_entry = {
            'itemname': item['name'],
            'itemdescription': item.get('description', ''),
            'price': item.get('price', ''),
            'itemrank': '',
            'instock': '',
            'item_image_url': '',
            'variation': item.get('variations', []),
            'addon': []
        }
        for ref_item in json_ref['items']:
            if ref_item['itemname'].lower() == item['name'].lower():
                item_entry.update(ref_item)
                # Update price if extracted has it
                if item.get('price'):
                    item_entry['price'] = item['price']
                break
        mapped['items'].append(item_entry)
    return mapped

def save_to_excel(mapped_data, template_path, output_path):
    """Format mapped data into the provided Excel template."""
    try:
        wb = openpyxl.load_workbook(template_path)
        ws = wb.active
    except Exception as e:
        print(f"Error loading template: {e}. Creating new workbook.")
        wb = openpyxl.Workbook()
        ws = wb.active
    # Assume appending to existing sheet
    row = ws.max_row + 1
    # Write restaurant if not present
    if ws.max_row == 1:  # Assuming header
        ws[f'A{row}'] = 'Restaurant Name'
        ws[f'B{row}'] = mapped_data['restaurant']['restaurantname']
        row += 1
        ws[f'A{row}'] = 'Area ID'
        ws[f'B{row}'] = mapped_data['areas'][0]['areaid'] if mapped_data['areas'] else ''
        row += 1
        ws[f'A{row}'] = 'Area Name'
        ws[f'B{row}'] = mapped_data['areas'][0]['displayname'] if mapped_data['areas'] else ''
        row += 1
    # Categories
    ws[f'A{row}'] = 'Categories'
    row += 1
    ws[f'A{row}'] = 'ID'
    ws[f'B{row}'] = 'Name'
    ws[f'C{row}'] = 'Availability'
    ws[f'D{row}'] = 'Rank'
    row += 1
    for cat in mapped_data['categories']:
        ws[f'A{row}'] = cat.get('categoryid', '')
        ws[f'B{row}'] = cat.get('categoryname', '')
        ws[f'C{row}'] = cat.get('active', '')
        ws[f'D{row}'] = cat.get('categoryrank', '')
        row += 1
    # Items
    ws[f'A{row}'] = 'Items'
    row += 1
    ws[f'A{row}'] = 'Name'
    ws[f'B{row}'] = 'Description'
    ws[f'C{row}'] = 'Price'
    ws[f'D{row}'] = 'Rank'
    ws[f'E{row}'] = 'Stock Status'
    row += 1
    for item in mapped_data['items']:
        ws[f'A{row}'] = item.get('itemname', '')
        ws[f'B{row}'] = item.get('itemdescription', '')
        ws[f'C{row}'] = item.get('price', '')
        ws[f'D{row}'] = item.get('itemrank', '')
        ws[f'E{row}'] = item.get('instock', '')
        row += 1
    wb.save(output_path)

def main():
    json_path = 'data_reference.json'
    template_path = 'Python Dev Task Sample.xlsx'
    output_path = 'output_final.xlsx'
    image_paths = ['task_menu_1.png', 'task_menu_2.png']

    json_ref = load_json_reference(json_path)
    all_extracted = {'categories': [], 'items': []}

    for img_path in image_paths:
        text = extract_text_from_image(img_path)
        print(f"Extracted text from {img_path}:\n{text}\n")
        data = parse_menu_text(text)
        all_extracted['categories'].extend(data['categories'])
        all_extracted['items'].extend(data['items'])

    mapped_data = map_data(all_extracted, json_ref)
    save_to_excel(mapped_data, template_path, output_path)
    print(f"Process completed. Output saved to {output_path}")

if __name__ == "__main__":
    main()
