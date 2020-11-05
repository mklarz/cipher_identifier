#!/usr/bin/python
import glob
import os
import pathlib
import re
import urllib.parse

md_text = "# Cipher list\n"

BASE_URL = "https://www.dcode.fr"
BASE_PATH = pathlib.Path(__file__).resolve().parents[1].absolute()
CIPHERS_PATH = "{}/ciphers".format(BASE_PATH)
CIPHERS = sorted(next(os.walk(CIPHERS_PATH))[1])
GITHUB_IMAGE_PATH_FORMAT = "./ciphers/{}/combined.png"

for cipher in CIPHERS:
    md_text += "\n### [{}]({}/{})\n".format(cipher, BASE_URL, cipher)
    image_url = GITHUB_IMAGE_PATH_FORMAT.format(cipher)
    md_text += "![{}]({})".format(cipher, image_url)

with open("CIPHERS.md", "w") as f:
    f.write(md_text)
