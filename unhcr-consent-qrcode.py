import PyPDF2
import qrcode
from io import BytesIO
import os
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


# Open the PDF file to be duplicated
pdf_file = open('UNHCR-Study-CONSENT-FORM.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Create a PDF writer object to write the output
pdf_writer = PyPDF2.PdfWriter()

# Loop through each page in the PDF and duplicate it with a unique QR code
for page_num in range(len(pdf_reader.pages)):
    # Create a new page with the same dimensions as the original page
    page = pdf_reader.pages[page_num]
    output_page = pdf_writer.add_blank_page(page.mediabox.width, page.mediabox.height)

    # Add the original content to the new page
    output_page.merge_page(page)

    # Generate a unique QR code and add it to the top right corner of the page
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data('UN23{:04d}'.format(page_num+1))
    qr.make(fit=False)
    img = qr.make_image(fill_color='black', back_color='white', method='basic', optimize=0, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, image_factory=None, mask_pattern=None, quiet_zone=4, fit=False, scale=1, background_color='white', foreground_color='black', encoding=None, language=None, mode=None, timeout=10)

    # Save the QR code image to a BytesIO buffer
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')

   # Read the QR code image from the BytesIO buffer and add it to the new page as an image
    img_pdf = ImageReader(img_bytes.getvalue())
    img_width, img_height = img_pdf.getSize()
    img_ratio = img_height / img_width
    img_x = page.mediabox.width - 50
    img_y = page.mediabox.height - (img_width * img_ratio) - 50

    # Create a new canvas and draw the image onto it
    canvas_obj = canvas.Canvas('temp.pdf', pagesize=(page.mediabox.width, page.mediabox.height))
    canvas_obj.drawImage(img_bytes.getvalue(), img_x, img_y, img_width, img_height)
    canvas_obj.save()

    # Get the page from the new canvas and merge it with the output page
    img_pdf = PyPDF2.PdfReader(open('temp.pdf', 'rb')).pages[0]
    output_page.merge_page(img_pdf)

    # Remove the temporary files
    #os.remove(img_file)
    os.remove('temp.pdf')

# Write the output PDF to a new file
output_file = open('UNHCR-Study-CONSENT-FORM-QRCODE.pdf', 'wb')
pdf_writer.write(output_file)

# Close the input and output files
pdf_file.close()
output_file.close()
