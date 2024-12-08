import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Paths
input_pdf = "Input_Certificate.pdf"
output_pdf = "Updated_Certificate.pdf"
overlay_pdf = "Text_Overlay.pdf"
sorts_mill_goudy_font = "SortsMillGoudy-Italic.ttf"
alex_brush_font = "AlexBrush-Regular.ttf"

# Define text and their positions
texts = [
    ("Adventurer", "SortsMillGoudy", 53, (217.66, 428.03)),  # Text, Font, Size, Position (x, y)
    ("Frank", "AlexBrush", 80, (272.11, 335.97))
]

# Step 1: Register Fonts
def register_fonts():
    try:
        pdfmetrics.registerFont(TTFont("SortsMillGoudy", sorts_mill_goudy_font))
        pdfmetrics.registerFont(TTFont("AlexBrush", alex_brush_font))
        print("Fonts registered successfully.")
    except Exception as e:
        print(f"Failed to register fonts: {e}")

# Step 2: Create the text overlay PDF using reportlab
def create_text_overlay(output_path, texts, page_width, page_height):
    from reportlab.lib.pagesizes import landscape

    # Adjust page size to match the input PDF
    page_size = (page_width, page_height)

    c = canvas.Canvas(output_path, pagesize=page_size)

    # Add text to the canvas
    for text, font_name, font_size, position in texts:
        try:
            c.setFont(font_name, font_size)  # Use the registered font name
        except KeyError:
            print(f"Font '{font_name}' not found. Using default Helvetica.")
            c.setFont("Helvetica", font_size)  # Fallback to Helvetica
        x, y = position
        c.drawString(x, y, text)  # Draw the text at the specified position
    
    c.save()

# Step 3: Merge the overlay with the original PDF using PyMuPDF
def merge_pdfs(input_pdf, overlay_pdf, output_pdf):
    original = fitz.open(input_pdf)
    overlay = fitz.open(overlay_pdf)
    
    for page_num in range(len(original)):
        page = original[page_num]
        if page_num < len(overlay):
            overlay_page = overlay[page_num]
            page.show_pdf_page(page.rect, overlay, page_num)  # Merge overlay
    original.save(output_pdf)

# Register fonts
register_fonts()

# Step 4: Get page size and generate overlay
def get_page_size(input_pdf):
    doc = fitz.open(input_pdf)
    first_page = doc[0]
    width, height = first_page.rect.width, first_page.rect.height
    doc.close()
    return width, height

page_width, page_height = get_page_size(input_pdf)
create_text_overlay(overlay_pdf, texts, page_width, page_height)

# Merge the PDFs
merge_pdfs(input_pdf, overlay_pdf, output_pdf)

print(f"Updated certificate saved to {output_pdf}")
