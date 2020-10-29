#!/usr/bin/python
import os
import re
import cv2
import pathlib
import requests
import argparse
import numpy as np

BASE_PATH = "{}/ciphers".format(pathlib.Path(__file__).resolve().parents[1].absolute())
BASE_URL = "https://www.dcode.fr"
HOME_MESSAGE = "dCode</a> offers tools to win for sure, for example the <"

def crop_image(img):
    # https://stackoverflow.com/a/49907762
    # Modified to check borders
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
    if not gray.any():
        # Found no borders, return original image
        return img
    coords = cv2.findNonZero(gray) # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
    rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
    return rect

def image_sizes_are_identical(images):
    last_size = None
    for image in images:
        height, width, channels = image.shape
        image_size = (height, width)
        if last_size is not None and last_size != image_size:
            return False
        last_size = image_size
    else:
        return True

def download_cipher_images(cipher, redownload=False):
    cipher_base_path = "{}/{}".format(BASE_PATH, cipher)

    # Check if cipher exists
    if not redownload and os.path.exists(cipher_base_path):
        print("[WARNING] Cipher '{}' exists in {}, ignoring cipher.".format(cipher, BASE_PATH))
        print("Use the redownload arugment (-r, --redownload) to force a redownload")
        return

    cipher_images_path = "{}/images".format(cipher_base_path)

    # Find the images
    url = requests.utils.requote_uri("{}/{}".format(BASE_URL, cipher))
    print("Trying to look up cipher URL:", url)
    r = requests.get(url, headers={"User-agent": "scrape"})
    content = r.content.decode()

    # Check if the cipher is valid
    if HOME_MESSAGE in content:
        print("[ERROR] Could not find a URL for cipher '{}'".format(cipher))
        print("Tried URL:", url)
        exit(1)

    js_string = re.findall(r'\<script\>\$\.cryptoarea\.path \= \'(.*?)\<\/script\>', content)
    if len(js_string) == 0:
        print("[ERROR] Could not extract the JS to find the images")
        exit(1)

    string_split = js_string[0].split(";")

    # Extract out images url, i.e. https://www.dcode.fr/tools/stargate-ancients/images
    images_url = string_split[0][:-1]

    # Find the array of char(x).
    match = re.search(r'\[(.*?)\]', string_split[1]).group(1)
    # Find all char(x).png (pictures of the symbols).
    chars = re.findall(r'\((.*?)\)', match)

    # Create directory if it doesn't exist
    os.makedirs(cipher_images_path, exist_ok=True)

    raw_images = {}
    images_downloaded = set()
    for char in chars:
        # i here is the ASCII number for the character
        i = int(char)

        # Don't download images twice
        if i in images_downloaded:
            continue

        image_filename = "{}.png".format(i)
        image_urlname = "char({}).png".format(i)
        image_path = "{}/{}".format(cipher_images_path, image_filename)
        image_url = "{}/{}".format(images_url, image_urlname)
        print("Fetching image: '{}' and saving it to {}".format(image_urlname, cipher_images_path))
        r = requests.get(image_url)

        if r.status_code != 200:
            print("[ERROR] Something went wrong when downloading image, status code: {}".format(r.status_code))
            exit(1)

        # Save the images for now, might need to overwrite them if they have borders
        with open(image_path, "wb") as f:
            f.write(r.content)

        raw_images[image_path] = r.content
        images_downloaded.add(i)

    images = {}

    # Read the images into CV2 objects
    for image_path, image_bytes in raw_images.items():
        # Read the image into CV2
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        images[image_path] = image

    # TODO: Handle this another way, we need to remove the white background for identical images as well
    """
    if not image_sizes_are_identical(images.values()):
        print("Images are not unique, performing border/padding removal")
        # Process the images if their sizes are NOT identical,
        # meaning they most likely have padding (borders) added

    """
    for image_path, image in images.items():
        # Crop the image (remove borders i.e.)
        image = crop_image(image)

        # For debugging, show the image
        """
        cv2.imshow('image',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(0)
        """ 
        cv2.imwrite(image_path, image)

    print("Done!")

example_text = """Examples:
 # Download images for a specific cipher (-c, --cipher)
 download_images.py -c ancients-stargate-alphabet
 # Download images for all (-a, --all) the images specified in the ciphers file
 download_images.py -a
 # Specify which ciphers file to use, needs to contain a list of the cipher names
 download_images.py -a -cf ciphers.txt
 # Force redownload of images for a cipher, even if they exist
 download_images.py -r -c ancients-stargate-alphabet
 # Force redownload of all ciphers and their images, even if they exist
 download_images.py -r -a"""

parser = argparse.ArgumentParser(
    prog="download_images",
    description="Download cipher images from dcode.fr",
    epilog=example_text,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "-c", "--cipher",
    help="the name of the cipher to download images from"
)
parser.add_argument(
    "-cf", "--ciphers-file", default="ciphers.txt",
    help="file containing the list of ciphers"
)
parser.add_argument(
    "-a", "--all", default=False, const=True, nargs='?',
    help="download all the ciphers specified in the ciphers file"
)
parser.add_argument(
    "-r", "--redownload", default=False, const=True, nargs='?',
    help="force redownload of ciphers and their images."
)

args = parser.parse_args()

if not args.cipher and not args.all:
    # Neither the cipher is specified and the --all parameter is False
    print("[ERROR] Need to specify a cipher or use the --all parameter")
    print(example_text)
    exit(1)

if args.cipher:
    cipher = args.cipher
    # Download images for a single cipher
    download_cipher_images(cipher, redownload=args.redownload)
else:
    # Download images for all the ciphers
    ciphers_file = args.ciphers_file
    if not os.path.exists(ciphers_file):
        print("[ERROR] Ciphers file does not exist:", ciphers_file)
        exit(1)

    with open(ciphers_file) as f:
        ciphers = f.read().splitlines()
        print("Loaded {} ciphers".format(len(ciphers)))
        for cipher in ciphers:
            download_cipher_images(cipher, redownload=args.redownload)
