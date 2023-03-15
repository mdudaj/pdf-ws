import os
import labels
from reportlab.graphics import shapes
from reportlab.graphics.barcode import code128, qr
from reportlab.lib.units import mm

# Create an A4 portrait (210mm x 297mm) sheet with 13 rows and 5 columns of labels.
# Each label is 38.1mm x 21.2mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(210, 297, 5, 13, 37.5, 21.2, corner_radius=2)

# Define starting and ending barcode codes
STARTING_CODE = 230001
ENDING_CODE = 231200

# Set barcode dimensions
barcode_height = 50
barcode_width = 0.8

# Create a function to draw each label.
def draw_label(label, width, height, obj):
    barcode_value = "UNHCR" + str(obj)
    size = 14 * mm
    qr_code = qr.QrCodeWidget(barcode_value, barHeight=height, barWidth=size, barBorder=2)
    # Calculate the position to center the barcode on the label
    barcode_x = (width - barcode_width * size) / 2
    barcode_y = (height - barcode_height) / 2
    qr_code.x = barcode_x
    qr_code.y = barcode_y
    label.add(qr_code) # Add the barcode image to the label
    label.add(shapes.String(20, height-55, barcode_value, fontName='Helvetica', fontSize=10)) # Add the barcode value tag below the barcode

# Create the sheet.
sheet = labels.Sheet(specs, draw_label, border=True)

# Generate labels for the range UNHCR230001 to UNHCR231100.
labels_list = [str(code) for code in range(STARTING_CODE, ENDING_CODE + 1)]
sheet.add_labels(labels_list)

# Create the output folder if it doesn't exist.
if not os.path.exists("barcode-tags"):
    os.makedirs("barcode-tags")

# Save the file and we are done.
with open(os.path.join("barcode-tags", "barcodes.pdf"), "wb") as f:
    sheet.save(f)

print(
    "{0:d} label(s) output on {1:d} page(s).".format(
        sheet.label_count, sheet.page_count
    )
)
