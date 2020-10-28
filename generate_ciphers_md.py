#!/usr/bin/python
import re
import os
import glob
import pathlib
import urllib.parse

md_text = "# Cipher list\n"

BASE_URL = "https://www.dcode.fr"
BASE_PATH = pathlib.Path(__file__).parent.absolute()
CIPHERS_PATH = "{}/ciphers".format(BASE_PATH)
CIPHERS = sorted(next(os.walk(CIPHERS_PATH))[1])
GITHUB_IMAGE_PATH_FORMAT = "./ciphers/{}/images/{}"

for cipher in CIPHERS:
    md_text += "\n### [{}]({}/{})\n".format(cipher, BASE_URL, cipher)
    images = sorted(glob.glob("{}/{}/images/*.png".format(CIPHERS_PATH, cipher)))
    for image in images:
        filename = os.path.basename(image)
        image_url = GITHUB_IMAGE_PATH_FORMAT.format(cipher, filename)
        i = int(re.search(r'char\((.*?)\)', filename).group(1))
        c = urllib.parse.quote(chr(i))
        alt_text = "{} ({})".format(c, i)
        md_text += "![{}]({}) ".format(alt_text, image_url)

with open("CIPHERS.md", "w") as f:
    f.write(md_text)
