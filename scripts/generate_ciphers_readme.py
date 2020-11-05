#!/usr/bin/python
import glob
import json
import os
import pathlib
import re
import urllib.parse

BASE_PATH = pathlib.Path(__file__).resolve().parents[1].absolute()
CIPHERS_PATH = "{}/ciphers".format(BASE_PATH)
CIPHERS = sorted(next(os.walk(CIPHERS_PATH))[1])

for cipher in CIPHERS:
    cipher_path = "./ciphers/{}".format(cipher)
    with open("{}/cipher.json".format(cipher_path)) as f:
        info = json.load(f)

    md_text = "# {}\n".format(info["title"])
    md_text += "{}\n\n".format(info["description"])
    md_text += "#### Charset: `{}`\n\n".format(info["charset_information"]["charset"])
    md_text += "#### Tags: `{}`\n\n".format(", ".join(info["tags"]))
    md_text += "#### Source: {}\n\n".format(info["source_url"])
    md_text += "![combined](./combined.png)\n\n"
    md_text += "### Questions\n\n"

    for item in info["questions"]:
        md_text += "#### {}\n".format(item["question"])
        md_text += "{}\n\n".format(item["answer"])

    with open("{}/README.md".format(cipher_path), "w") as f:
        f.write(md_text)
