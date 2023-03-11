# Import required modules
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128

# Define starting and ending barcode codes
STARTING_CODE = 230001
ENDING_CODE = 231100

# Set barcode dimensions
barcode_height = 30
barcode_width = 1.2

# Create the consent-forms directory if it doesn't exist
if not os.path.exists("consent-forms"):
    os.makedirs("consent-forms")

# Create a list to hold the output PDF files
output_files = []

for code in range(STARTING_CODE, ENDING_CODE+1):
    # Define barcode code and position variables
    BARCODE_CODE = f"UNHCR{code}"
    x_var = 70
    y_var = 260

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
    output_file_name = f"UNHCR-Study-CONSENT-FORM-WITH-CODE128-{BARCODE_CODE}.pdf"
    output_file_path = os.path.join("consent-forms", output_file_name)
    outputStream = open(output_file_path, "wb")
    output.write(outputStream)
    outputStream.close()

    print(f"{output_file_name} created successfully!")
    
    # Add the output PDF file to the list
    output_files.append(output_file_path)

# Merge all the output PDF files into a single PDF
merged_output = PdfFileWriter()

for file in output_files:
    pdf = PdfFileReader(open(file, "rb"))
    for page in range(pdf.getNumPages()):
        merged_output.addPage(pdf.getPage(page))

# Write the merged output PDF to a file
merged_output_file_name = "UNHCR-Study-CONSENT-FORMS-WITH-CODE128.pdf"
merged_output_file_path = os.path.join("consent-forms", merged_output_file_name)
merged_output_stream = open(merged_output_file_path, "wb")
merged_output.write(merged_output_stream)
merged_output_stream.close()

print(f"All output PDF files merged into {merged_output_file_name} successfully!")
