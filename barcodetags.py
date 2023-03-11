import os
import labels
from reportlab.graphics.barcode import code128, qr
from reportlab.lib.units import mm

# Create an A4 portrait (210mm x 297mm) sheet with 13 rows and 5 columns of labels.
# Each label is 38.1mm x 21.2mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(210, 297, 5, 13, 37.5, 21.2, corner_radius=2)

# Define starting and ending barcode codes
STARTING_CODE = 230001
ENDING_CODE = 231100

# Set barcode dimensions
barcode_height = 20
barcode_width = 0.8

# Create a function to draw each label.
def draw_label(label, width, height, obj):
    barcode_value = "UNHCR" + str(obj)
    # barcode128 = code128.Code128(barcode_value, barHeight=barcode_height, barWidth=barcode_width)
    # barcode128.drawOn(label, 5, 2)
    size = 12 * mm
    label.add(
        qr.QrCodeWidget(barcode_value, barHeight=height, barWidth=size, barBorder=2)
    )


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
