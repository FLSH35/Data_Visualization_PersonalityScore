# -*- coding: utf-8 -*-
import re
import fitz  # PyMuPDF

def extract_order_data(pdf_path):
    # Open the PDF document
    document = fitz.open(pdf_path)
    extracted_data = []

    for page_num in range(len(document)):
        # Extract text from the current page
        page_text = document[page_num].get_text()

        # Regex patterns to match the relevant information
        order_fee_pattern = r"Orderkosten.*?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)) EUR"
        quantity_pattern = r"Kauf:\s*(\d+)\s*Stück"
        id_pattern = r"WKN:\s*([A-Z0-9]+)"
        datetime_pattern = r"(\d{2}\.\d{2}\.\d{4}\s*-\s*\d{2}:\d{2}\s*Uhr)"
        price_pattern = r"Kurswert:\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)) EUR"

        # Extract data using regex patterns
        order_fee = re.search(order_fee_pattern, page_text)
        quantity = re.search(quantity_pattern, page_text)
        identifier = re.search(id_pattern, page_text)
        datetime = re.search(datetime_pattern, page_text)
        price = re.search(price_pattern, page_text)

        # Structure the extracted data
        data = {
            "Ordergebühren": order_fee.group(1) if order_fee else None,
            "Anzahl der gekauften Wertpapiere": quantity.group(1) if quantity else None,
            "Wertpapier-Identifikator": identifier.group(1) if identifier else None,
            "Datum und Uhrzeit des Kaufs": datetime.group(1) if datetime else None,
            "Kurswert": price.group(1) if price else None,
        }
        extracted_data.append(data)

    document.close()
    return extracted_data

# Define the path to the uploaded PDF file
pdf_path = "aktien.pdf"

# Extract data
order_data = extract_order_data(pdf_path)

# Display the extracted data
for entry in order_data:
    print(entry)
