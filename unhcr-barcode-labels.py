import os
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileMerger

# Define the starting and ending label numbers
start_label = 230001
end_label = 231100

# Calculate the total number of labels to be printed
num_labels = end_label - start_label + 1

# Calculate the number of rows and columns needed to print all the labels
num_rows = 13
num_cols = 5
num_labels_per_page = num_rows * num_cols
num_pages = num_labels // num_labels_per_page + (1 if num_labels % num_labels_per_page != 0 else 0)

# Create the output directory if it doesn't exist
if not os.path.exists('barcode-labels'):
    os.mkdir('barcode-labels')

# Initialize the PDF merger object
merger = PdfFileMerger()

# Generate the barcode labels and add them to the PDF merger object
for page in range(num_pages):
    # Create a new PDF canvas with landscape A4 size
    c = canvas.Canvas(f'barcode-labels/labels-page-{page+1}.pdf', pagesize=landscape(A4))

    # Set the font size and position for the label text
    c.setFont('Helvetica', 10)
    x_text = 15 * mm
    y_text = 5 * mm

    # Generate the barcode labels for this page
    for i in range(num_rows):
        for j in range(num_cols):
            label_num = start_label + page * num_labels_per_page + i * num_cols + j
            if label_num > end_label:
                break

            # Generate the barcode image
            barcode = code128.Code128(f'UNHCR{label_num}', humanReadable=True, barHeight=10 * mm, barWidth=0.25 * mm)

            # Draw the barcode image and label text on the canvas
            x_barcode = j * 40 * mm + 20 * mm
            y_barcode = i * 20 * mm + 15 * mm
            barcode.drawOn(c, x=x_barcode, y=y_barcode)
            c.drawString(x_text, y_text, f'UNHCR{label_num}')

        # Move to the next row
        x_text = 15 * mm
        y_text += 20 * mm

    # Save the PDF canvas to a file
    c.save()

    # Add the generated PDF page to the PDF merger object
    merger.append(f'barcode-labels/labels-page-{page+1}.pdf')

# Write the final merged PDF file to disk
merger.write(open('barcode-labels/all-labels.pdf', 'wb'))
