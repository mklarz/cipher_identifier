#!/usr/bin/python
import glob
import os
import json
import pathlib
import re
import urllib.parse

md_text = "# Cipher list\n"

BASE_PATH = pathlib.Path(__file__).resolve().parents[1].absolute()
CIPHERS_PATH = "{}/ciphers".format(BASE_PATH)
CIPHERS = sorted(next(os.walk(CIPHERS_PATH))[1])
GITHUB_CIPHER_PATH_FORMAT = "./ciphers/{}"

for cipher in CIPHERS:
    cipher_path = "./ciphers/{}".format(cipher)
    with open("{}/cipher.json".format(cipher_path)) as f:
        cipher_title = json.load(f)["title"]

    md_text += "\n### [{}]({})\n".format(cipher_title, cipher_path)
    image_url = "{}/combined.png".format(cipher_path)
    md_text += "![{}]({})".format(cipher, image_url)

with open("CIPHERS.md", "w") as f:
    f.write(md_text)
