# Import required modules
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128

# Define barcode code and position variables
BARCODE_PREFIX = "UNHCR"
BARCODE_START_NUM = 230001
BARCODE_END_NUM = 231100
x_var = 70
y_var = 260

# Set barcode dimensions
barcode_height = 30
barcode_width = 1.2

# Create a buffer to store PDF file in memory
packet = BytesIO()

# Create a canvas object
slab = canvas.Canvas(packet, pagesize=A4)

# Set font color to black
slab.setFillColorRGB(0, 0, 0)

# Open the existing PDF file
with open("UNHCR-Study-CONSENT-FORM.pdf", "rb") as existing_pdf_file:
    # Read the existing PDF
    existing_pdf = PdfFileReader(existing_pdf_file)
    # Get the first page
    first_page = existing_pdf.getPage(0)
    # Get the merged page with the first barcode
    merged_page = None
    for i in range(first_page.mergePage(PdfFileReader(packet).getPage(0))):
        merged_page = first_page if i == 0 else existing_pdf.getPage(i)
    # Create copies of the merged pages for each barcode
    merged_pages = [merged_page] * (BARCODE_END_NUM - BARCODE_START_NUM + 1)

    # Loop through all barcode numbers and add them to the output PDF
    for i, barcode_num in enumerate(range(BARCODE_START_NUM, BARCODE_END_NUM+1)):
        
        # Generate the barcode code
        barcode_code = f"{BARCODE_PREFIX}{barcode_num:06}"
        
        # Generate the barcode
        barcode = code128.Code128(barcode_code, humanReadable=True, barHeight=barcode_height, barWidth=barcode_width)
        
        # Draw the barcode on the canvas
        slab.save()
        slab.restoreState()
        barcode.drawOn(slab, x_var * mm, y_var * mm)
        
        # Move the buffer to the beginning
        packet.seek(0)
        
        # Create a PDF object with the generated barcode
        new_pdf = PdfFileReader(packet)
        
        # Merge the barcode with the existing PDF pages
        for j in range(len(merged_pages)):
            merged_pages[j] = merged_pages[j].mergePage(new_pdf.getPage(0))
        
        # Reset the buffer
        packet.seek(0)
        packet.truncate(0)
        
    # Create the output PDF object
    output = PdfFileWriter()
    
    # Add all merged pages to the output PDF
    for page in merged_pages:
        output.addPage(page)
    
    # Write the output PDF to a file
    outputStream = open("UNHCR-Study-CONSENT-FORM-WITH-CODE128.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
