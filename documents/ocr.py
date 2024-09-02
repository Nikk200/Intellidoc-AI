import pytesseract, os
from PIL import Image
from pdf2image import convert_from_path

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path) #opening the image
        text = pytesseract.image_to_string(img) #extracting the text from image using pytesseract
        return text
    except Exception as e:
        print(f'Error in OCR: {e}')
        return None

def extract_text_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
    except Exception as e:
        return
    text = ""
    for img in images:
        img.save("page.png", "PNG")
        text += pytesseract.image_to_string(Image.open("page.png"), lang='eng', config='--psm 11')
        os.remove("page.png")
    return text

