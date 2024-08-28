from django.test import TestCase

# Create your tests here.

import cv2
from PIL import Image
import pytesseract
from matplotlib import pyplot as plt

img_file = 'intellidoc_ai//sample_documents//2.png'

img = cv2.imread(img_file) #loading image to memory

def display_image(im_path):

    dpi = 80
    im_data = plt.imread(im_path)
    height, width = im_data.shape

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()

# display_image("intellidoc_ai//temp//bw_image_2.png")


#Inverting an image
# inverted_image = cv2.bitwise_not(img)
# cv2.imwrite("intellidoc_ai//temp//bitwise_not_2.png", inverted_image)


#Binarization
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_image = grayscale(img)
# cv2.imwrite("intellidoc_ai//temp/gray_image_2.png", gray_image)


thresh, im_bw = cv2.threshold(gray_image, 200, 230, cv2.THRESH_BINARY)
# cv2.imwrite("intellidoc_ai//temp/bw_image_2.png", gray_image)



# Noise Removal
def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode((1, 1), kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

# no_noise = noise_removal(im_bw)
# cv2.imwrite("intellidoc_ai//temp//no_noise.png", no_noise)


# Dilation & Erosion
# Erosion is thinning of pixels
# Dilation is thikening of pixels
# Dilation and Erosion works on black bg and white text images (often)

def thin_font(image): #Erosion
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

# eroded_image = thin_font(no_noise)
# cv2.imwrite("intellidoc_ai//temp//eroded_image_2.png", eroded_image)



def thin_font(image): #Dilation
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

# eroded_image = thin_font(no_noise)
# cv2.imwrite("intellidoc_ai//temp//eroded_image_2.png", eroded_image)



# Rotation/Deskewing

new_image = cv2.imread("intellidoc_ai//sample_documents//p3.jpg")
# Calculate skew angle of an image
def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)


# fixed_image = deskew(new_image)
# cv2.imwrite("intellidoc_ai//temp//fixed_image.jpg", fixed_image)


# =======================================================================
# Introduction to pytesseract
img_file = "intellidoc_ai//sample_documents//p3.jpg"
no_noise = "intellidoc_ai//temp//bw_image_2.png"

img = Image.open(img_file)
# ocr_results = pytesseract.image_to_string(img) #no noise image will be needed for this to work
# print(ocr_results)













