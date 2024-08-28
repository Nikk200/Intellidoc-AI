from django.test import TestCase

# Create your tests here.

import cv2
import numpy as np
from PIL import Image
import pytesseract

def assess_image_quality(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to see if binarization is effective
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Calculate the number of white pixels (text) in the thresholded image
    white_pixels = np.sum(thresh == 255)
    total_pixels = thresh.shape[0] * thresh.shape[1]
    
    # Simple heuristic: If more than 50% of pixels are white, consider the image clear
    if white_pixels / total_pixels > 0.5:
        return False  # No preprocessing needed
    else:
        return True  # Preprocessing needed


def check_blur(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Laplacian to detect blur
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    variance = laplacian.var()
    
    # Simple heuristic: If variance is below a certain threshold, consider the image blurry
    if variance < 100:
        return True  # Image is blurry
    else:
        return False  # Image is not blurry

def preprocess_image(image_path):
    # Preprocessing steps (as described earlier)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("preprocessed_image.png", thresh)
    return "preprocessed_image.png"

def extract_text_from_document(file_path):
    if assess_image_quality(file_path) or check_blur(file_path):
        preprocessed_image_path = preprocess_image(file_path)
        text = pytesseract.image_to_string(Image.open(preprocessed_image_path), lang='eng', config='--psm 11')
    else:
        text = pytesseract.image_to_string(Image.open(file_path), lang='eng', config='--psm 11')
    return text


# import langdetect
# print(langdetect.detect("hello i am nikhil, how are you doing?"))

import torch
print(torch.__version__)