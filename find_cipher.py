#!/usr/bin/python
import os
import sys
import cv2
import glob
import time
import pathlib
import numpy as np

BASE_PATH = "{}/ciphers".format(pathlib.Path(__file__).parent.absolute())

if len(sys.argv) != 2:
    print("[ERROR] Invalid amount or no arguments")
    print("Example usage: python find_cipher.py image.png")
    exit(1)

image_path = sys.argv[1] 

if not os.path.exists(image_path):
    print("[ERROR] Could not find image:", image_path)
    exit(1)

IMG = cv2.imread(image_path)

ciphers = sorted(next(os.walk(BASE_PATH))[1])

# From https://stackoverflow.com/a/15147009 and modified
# Doc: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html?highlight=minmaxloc
def get_minimum_value(image):
    method = cv2.TM_SQDIFF_NORMED
    small_image = cv2.imread(image)
    large_image = IMG

    """
    Template Matching is a method for searching and finding the
    location of a template image in a larger image.
    OpenCV comes with a function cv2.matchTemplate() for this purpose.
    It simply slides the template image over the
    input image (as in 2D convolution) and compares the template
    and patch of input image under the template image. 
    Several comparison methods are implemented in OpenCV.
    (You can check docs for more details). 
    It returns a grayscale image, where each pixel denotes 
    how much does the neighbourhood of that pixel match with template.
    """
    result = cv2.matchTemplate(small_image, large_image, method)

    """
    If input image is of size (WxH) and template image is of size (wxh),
    output image will have a size of (W-w+1, H-h+1).
    Once you got the result, you can use cv2.minMaxLoc() function to fin
    where is the maximum/minimum value. 
    Take it as the top-left corner of rectangle and take (w,h) as width
    and height of the rectangle. That rectangle is your region of template.
    """
    min_value,_,_,_ = cv2.minMaxLoc(result)

    return min_value

def calculate_weight(values):
    # TODO: tweak this to use an actual weight algo?
    weight = round(sum(values) / len(values), 3)
    return 0 if weight == 1 else weight

cipher_weights = {}
for cipher in ciphers:
    start = time.process_time()
    print("Checking:", cipher, end=" = ")
    cipher_path = "{}/{}".format(BASE_PATH, cipher)
    images_path = "{}/images".format(cipher_path)
    images = glob.glob("{}/*.png".format(images_path))
    image_count = len(images)

    values = []
    for index, filename in enumerate(images):
        values.append(get_minimum_value(filename))

    weight = calculate_weight(values)
    print(weight, end="")
    cipher_weights[cipher] = weight

    end = time.process_time() - start
    print(", took {} seconds".format(end))

# Sort the by weight
cipher_weights = {k: v for k, v in sorted(cipher_weights.items(), reverse=True, key=lambda item: item[1])}

print("=" * 32)
print("Top ciphers:")
for index, cipher in enumerate(cipher_weights):
    position = index + 1
    weight = cipher_weights[cipher]

    if weight == 0:
        # Not a match
        continue

    print(position, weight, cipher, sep="\t")

print("=" * 32)
