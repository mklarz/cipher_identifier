#!/usr/bin/python
import os
import math
import glob
import time
import json
import pathlib
import random
import numpy as np
from PIL import Image, ImageDraw

DEFAULT_IMAGE_MIN_SIZE = (450, 100) # (width, height)
DEFAULT_IMAGE_MAX_SIZE = (800, 300) # (width, height)
DEFAULT_IMAGE_MINMAX_SIZE = (DEFAULT_IMAGE_MIN_SIZE, DEFAULT_IMAGE_MAX_SIZE)

#############################################################################

BASE_PATH = pathlib.Path(__file__).resolve().parents[1].absolute()
TRAIN_DATA_PATH = "{}/models/train".format(BASE_PATH)
CIPHERS_PATH = "{}/ciphers".format(BASE_PATH)
CIPHERS = sorted(next(os.walk(CIPHERS_PATH))[1])

def get_random_image_size(image_minmax_size):
    return (
        random.randint(
            image_minmax_size[0][0], # min width
            image_minmax_size[1][0], # max width
        ),
        random.randint(
            image_minmax_size[0][0], # min height
            image_minmax_size[1][0], # max height
        ),
    )

def get_random_color():
    # Make sure we don't get a black image
    min_value = 10
    max_value = 256
    return (
        random.randrange(min_value, max_value), # R
        random.randrange(min_value, max_value), # G
        random.randrange(min_value, max_value), # B
        random.randrange(min_value, max_value), # A
    )

def is_overlap(l1, r1, l2, r2):
    # https://stackoverflow.com/a/54489667
    if l1[0] > r2[0] or l2[0] > r1[0]:
        return False

    if l1[1] > r2[1] or l2[1] > r1[1]:
        return False

    return True


def tesseract_box_string(character, left, bottom, right, top, page=0):
    # Tesseract box file.
    # Coordinates for ecah symbol in the iamge
    # NB! (0, 0) at bottom-left corner of the image!
    # See https://tesseract-ocr.github.io/tessdoc/Training-Tesseract-%E2%80%93-Make-Box-Files.html
    return "{} {} {} {} {} {}\n".format(
        character,
        left,
        bottom,
        right,
        top,
        page
    )

def generate_image(images, background_color=(255, 255, 255, 255), padding=5):
    """
    Find the width by summing the width of all the images (and padding)
    Find the height by finding the tallest image of the bunch
    """
    background_width = padding * 2
    background_height = 0
    for image in images:
        background_width += image.size[0] + padding
        if image.size[1] > background_height:
            background_height = image.size[1]
    background_height += padding * 2

    # Intialize the background image
    background_size = (background_width, background_height)
    background = Image.new('RGBA', background_size, background_color)
    x = padding
    y = padding

    # For tesseract, we need to map the coordinates for each symbol
    tesseract_boxes = ""
    for image in images:
        width, height = image.size

        # Find ASCII character and map its coordinates
        character = get_symbol_characters([image])
        tesseract_boxes += tesseract_box_string(
            character=character,
            left=x,
            bottom=background_height - y - height,
            right=x + width,
            top=background_height - y 
        )

        # Append the image to the symbol
        offset = (x, y)
        background.paste(image, offset, mask=image)
        x += width + padding

    return background, tesseract_boxes



# TODO: start using this
def place_images(images, image_minmax_size,  background_color=(255,255,255)):
    size = get_random_image_size(image_minmax_size)
    print("size={}".format(size), end=", ")

    # White background image
    background = Image.new('RGB', size, (255, 255, 255))

    # Random color to fade into the white background
    background_color = get_random_color()
    print("background_color={}".format(background_color), end=", ")
    foreground = Image.new('RGBA', size, background_color)

    # We now have our base image
    background.paste(foreground, (0, 0), foreground)

    # https://stackoverflow.com/a/54489667
    # and modified for random scale/ratio
    alread_paste_point_list = []
    for img in images:
        # Resize the image/symbol randomly
        seed = random.randint(1, 6)
        width = img.size[0]
        width += random.randint(
            width - (width // seed),
            width + (width // seed),
        )
        # To change the 1:1 scale
        # seed = random.randint(1, 6)
        height = img.size[1]
        height += random.randint(
            height - (height // seed),
            height + (height // seed),
        )
        img = img.resize((width, height), Image.ANTIALIAS)

        # TODO: Rotate?

        # if all not overlap, find the none-overlap start point
        while True:
            # left-top point
            # x, y = random.randint(0, background.size[0]), random.randint(0, background.size[1])

            # if image need in the bg area, use this
            x = random.randint(0, max(0, background.size[0] - img.size[0]))
            y = random.randint(0, max(0, background.size[1] - img.size[1]))

            # right-bottom point
            l2, r2 = (x, y), (x + img.size[0], y + img.size[1])

            if all(not is_overlap(l1, r1, l2, r2) for l1, r1 in alread_paste_point_list):
                # save alreay pasted points for checking overlap
                alread_paste_point_list.append((l2, r2))
                background.paste(img, (x, y), img)
                break

    return background

def generate_background_image(size, color):
    # White background image
    background = Image.new('RGB', size, (255, 255, 255))

def get_symbol_characters(symbols):
    # Map the ASCII codes to characters
    symbol_characters = ""
    for symbol in symbols:
        # Get the symbol number (ASCII code)
        d = int(os.path.basename(symbol.filename).replace(".png", ""))
        c = chr(d)
        symbol_characters += c
    return symbol_characters

def generate_random_symbols(images, divider=6):
    image_count = len(images)

    # How many symbols should we use?
    symbol_count = random.randint(
        (image_count // divider),
        image_count - (image_count // divider),
    )
    print("symbol_count={}".format(symbol_count), end=", ")

    random.shuffle(images)
    return images[0:symbol_count]


def generate_train_data(cipher, i=1000, image_minmax_size=DEFAULT_IMAGE_MINMAX_SIZE):
    cipher_path = "{}/{}".format(CIPHERS_PATH, cipher)
    cipher_images_path = "{}/images".format(cipher_path)
    train_images_path = "{}/{}".format(TRAIN_DATA_PATH, cipher)
    os.makedirs(train_images_path , exist_ok=True)
    image_paths = sorted(glob.glob("{}/*.png".format(cipher_images_path)))
    images = [Image.open(path) for path in image_paths]
    image_count = len(images)
    print("Cipher image count:", image_count)

    charset = "".join([chr(int(os.path.basename(path).replace(".png", ""))) for path in image_paths])
    digit_count = len(str(i))

    for nr in range(i):
        start_time = time.process_time()
        print("Generating image #{} [".format(nr + 1), end="")

        symbols = generate_random_symbols(images)
        image_characters = get_symbol_characters(symbols)
        train_filename = str(nr).zfill(digit_count) # 0000, 0001, 0002, etc.

        #operation = random.randint(1, 3)
        # TODO: remove, we only use the first operation now
        operation = 1
        print("operation={}".format(operation), end=", ")

        if operation == 1:
            # Combine the symbols into a new image and place it within the original image
            image, tesseract_boxes = generate_image(symbols)
        elif operation == 2:
            # Place x amount of symbols randomly around the image
            # TODO: enable again later?
            # image = place_images(symbols, image_minmax_size)
            pass
        
        # Save the image
        train_image_filename = "{}.png".format(train_filename)
        print("filename={}".format(train_image_filename), end=", ")
        image.save("{}/{}".format(train_images_path, train_image_filename))

        # Save the tesseract boxes
        with open("{}/{}.box".format(train_images_path, train_filename), "w") as f:
            f.write(tesseract_boxes)

        # TODO: tesseract
        # Plaintext file for tesseract
        with open("{}/{}.gt.txt".format(train_images_path, train_filename), "w") as f:
            f.write(image_characters)

        print("time_taken={}s".format(time.process_time() - start_time), end="]\n")


# TODO: only generate based on sysargv input, might be spammy to generate for all ciphers
print("Found {} ciphers".format(len(CIPHERS)))
for cipher in CIPHERS:
    print("Generating train images for cipher:", cipher)
    generate_train_data(cipher, i=1000)
