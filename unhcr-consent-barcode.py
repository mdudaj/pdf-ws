# Import required modules
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128

# Define barcode code and position variables
BARCODE_CODE = "UNHCR230001"
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

# Generate the barcode
barcode = code128.Code128(BARCODE_CODE, humanReadable=True, barHeight=barcode_height, barWidth=barcode_width)
barcode.drawOn(slab, x_var * mm, y_var * mm)

# Save the canvas object
slab.save()

# Move the buffer to the beginning
packet.seek(0)

# Create a PDF object with the generated barcode
new_pdf = PdfFileReader(packet)

# Read the existing PDF
existing_pdf = PdfFileReader(open("UNHCR-Study-CONSENT-FORM.pdf", "rb"))

# Create an output PDF object
output = PdfFileWriter()

# Add the barcode to all pages of the existing PDF
for i in range(existing_pdf.getNumPages()):
    page = existing_pdf.getPage(i)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

# Write the output PDF to a file
outputStream = open("UNHCR-Study-CONSENT-FORM-WITH-CODE128.pdf", "wb")
output.write(outputStream)
outputStream.close()