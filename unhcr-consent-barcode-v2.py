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

# Create an output PDF object
output = PdfFileWriter()

# Read the existing PDF
existing_pdf = PdfFileReader(open("UNHCR-Study-CONSENT-FORM.pdf", "rb"))

# Loop through all barcode numbers and add them to the output PDF
for barcode_num in range(BARCODE_START_NUM, BARCODE_END_NUM+1):
    
    # Generate the barcode code
    barcode_code = f"{BARCODE_PREFIX}{barcode_num:06}"
    
    # Generate the barcode
    barcode = code128.Code128(barcode_code, humanReadable=True, barHeight=barcode_height, barWidth=barcode_width)
    
    # Draw the barcode on the canvas
    barcode.drawOn(slab, x_var * mm, y_var * mm)
    
    # Save the canvas object
    slab.save()
    
    # Move the buffer to the beginning
    packet.seek(0)
    
    # Create a PDF object with the generated barcode
    new_pdf = PdfFileReader(packet)
    
    # Add the barcode to all pages of the existing PDF
    for i in range(existing_pdf.getNumPages()):
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
    
    # Reset the buffer
    packet = BytesIO()
    
    # Reset the canvas object
    slab = canvas.Canvas(packet, pagesize=A4)
    
    # Set font color to black
    slab.setFillColorRGB(0, 0, 0)

# Close the existing PDF file
existing_pdf.close()

# Write the output PDF to a file
outputStream = open("UNHCR-Study-CONSENT-FORM-WITH-CODE128.pdf", "wb")
output.write(outputStream)
outputStream.close()
