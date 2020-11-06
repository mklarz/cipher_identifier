#!/usr/bin/python
import argparse
import collections
import glob
import json
import math
import os
import pathlib
import random
import time

import numpy as np
from PIL import Image, ImageDraw

DEFAULT_IMAGE_MIN_SIZE = (450, 100)  # (width, height)
DEFAULT_IMAGE_MAX_SIZE = (800, 300)  # (width, height)
PADDING_MIN_MAX = (1, 4)
SPACE_PADDING_MIN_MAX = (5, 10)
DEFAULT_IMAGE_MINMAX_SIZE = (DEFAULT_IMAGE_MIN_SIZE, DEFAULT_IMAGE_MAX_SIZE)

SPACE_SYMBOL = None

#############################################################################

BASE_PATH = pathlib.Path(__file__).resolve().parents[1].absolute()
TRAIN_DATA_PATH = "{}/models/train".format(BASE_PATH)
CIPHERS_PATH = "{}/ciphers".format(BASE_PATH)
CIPHERS = sorted(next(os.walk(CIPHERS_PATH))[1])

# TODO: add additional sentences that should be used for each cipher
SENTENCES = ["The quick brown fox jumps over the lazy dog"]

CHARSET_LEETSPEAK_MAPPING = {
    "a": "4",
    "b": "8",
    "e": "3",
    "g": "6",
    "i": "1",
    "r": "2",
    "s": "5",
    "t": "7",
}

# TODO: need to add more
CHARSET_SYMBOL_MAPPING = {"a": "@", "e": "€", "i": "!", "s": "$"}


def transform_characters(sentence, sentence_charset, special_charset, chance=0.9):
    # Replace characters in the sentence with the specified charset (with a chance of swapping)
    sentence_lowercase = sentence.lower()
    sentence = list(sentence)

    for index, character in enumerate(sentence_lowercase):
        if (
            character not in special_charset
            or special_charset[character] not in sentence_charset
            or random.random() > chance
        ):
            continue
        sentence[index] = special_charset[character]

    return "".join(sentence)


def transform_sentence(sentence, sentence_charset, leetspeak=False, special=False):
    # Transform the sentence to use special characters as specified by the arguments
    transformed_sentence = None
    if leetspeak and special:
        transformed_sentence = transform_characters(
            sentence, sentence_charset, CHARSET_LEETSPEAK_MAPPING, chance=0.4
        )
        transformed_sentence = transform_characters(
            transformed_sentence, sentence_charset, CHARSET_SYMBOL_MAPPING
        )
    elif leetspeak:
        transformed_sentence = transform_characters(
            sentence, sentence_charset, CHARSET_LEETSPEAK_MAPPING
        )
    elif special:
        transformed_sentence = transform_characters(
            sentence, sentence_charset, CHARSET_SYMBOL_MAPPING
        )

    return (
        transformed_sentence
        if transformed_sentence and sentence != transformed_sentence
        else None
    )


def word_characters_exists_in_charset(word, charset, case_insensitive=False):
    if case_insensitive:
        word = word.lower()
        charset = charset.lower()

    for character in word:
        if character not in charset:
            # Character does not exist in the charset
            return False

    return True


def generate_sentences(
    charset,
    wordlist,
    limit,
    add_special_sentences=True,
    add_digit_sentences=True,
    digit_sentences_ratio=10,  # Everything 10th sentence will be digits only
):
    # Shuffle the provided wordlist and transform it into a Deque object
    random.shuffle(wordlist)
    wordlist = collections.deque(wordlist)

    # Lower the charset for more efficient substring comparison later
    charset_lowercase = charset.lower()

    # Check the characteristic of the charset
    # Most ciphers only include uppercase letters
    charset_has_lower = False
    charset_has_upper = False
    charset_has_digits = False
    charset_has_specials = False
    charset_digits = []
    for character in charset:
        if character.isdigit():
            charset_digits.append(character)
            charset_has_digits = True
        elif character.islower():
            charset_has_lower = True
        elif character.isupper():
            charset_has_upper = True
        else:
            # TODO: not character.isalnum()?
            charset_has_specials = True

    # Initialize required variables
    sentences = set()
    sentence_count = 0

    # Start generating the sentences
    while sentence_count < limit:
        # How many words do we want in the sentence
        sentence_word_count = random.randint(1, 6)

        if (
            add_digit_sentences
            and charset_has_digits
            and sentence_count % digit_sentences_ratio == 0
        ):
            # This sentence should be digits only
            digits = []
            for _ in range(sentence_word_count):
                digit_count = random.randint(4, 10)
                digits.append("".join(random.choices(charset_digits, k=digit_count)))
            sentence = " ".join(digits)
        else:
            current_words = set()
            current_word_count = 0
            while current_word_count < sentence_word_count:
                # Make sure we have enough words
                wordlist_length = len(wordlist)
                if wordlist_length == 0:
                    print("[ERROR] Wordlist ran out of words!")
                    exit(0)

                # Select the next word in our shuffled wordlist
                word = wordlist.pop()

                # Lowercase it for more efficient comparison
                word_lowercase = word.lower()

                # Check if the characters in the word exist in our charset
                if charset_has_lower and charset_has_upper:
                    """
                    If charset contains the uppercase of the first character in the word,
                    then randomly upper case it. If not we should use the lowercase word.
                    """
                    # Randomly captialize the first character if it exists in the charset:
                    c_upper = word[0].upper()
                    c_lower = word[0].lower()
                    if c_upper in charset and c_lower in charset:
                        # 50/50 chance to captialize the word
                        if random.random() > 0.5:
                            word = c_upper + word[1:]
                        else:
                            word = c_lower + word[1:]
                    elif c_upper in charset:
                        # Captialize the first character in the word
                        word = c_upper + word[1:]
                    elif c_lower in charset:
                        # Lowercase the word
                        word = word_lowercase
                    else:
                        continue

                    if not word_characters_exists_in_charset(
                        word, charset
                    ):
                        # A character in the word does not exist in our charset, skip this word and continue
                        continue
                else:
                    if not word_characters_exists_in_charset(
                        word_lowercase, charset_lowercase
                    ):
                        # A character in the word does not exist in our charset, skip this word and continue
                        continue

                    if not charset_has_lower:
                        # Charset does not have any lowercase words, let's uppercase the current word
                        word = word.upper()
                    elif not charset_has_upper:
                        # Charset does not have any uppercase words, let's use the lowercase one
                        word = word_lowercase

                current_words.add(word)
                current_word_count += 1

            sentence = " ".join(current_words)

        # Add the sentence to our list of sentences
        sentences.add(sentence)
        sentence_count += 1

        if (
            add_special_sentences
            and sentence_count < limit
            and sentence_count % digit_sentences_ratio != 0
            and (charset_has_digits or charset_has_specials)
        ):
            # Let's add additional a special (typical CTF) sentence to the list
            special_sentence = transform_sentence(
                sentence,
                charset_lowercase,
                leetspeak=charset_has_digits,
                special=charset_has_specials,
            )

            # Add the sentence to the list if it's different from the original sentence
            if special_sentence and special_sentence != sentence:
                sentences.add(special_sentence)
                sentence_count += 1

    return sentences


def get_random_image_size(image_minmax_size):
    return (
        random.randint(
            image_minmax_size[0][0], image_minmax_size[1][0]  # min width  # max width
        ),
        random.randint(
            image_minmax_size[0][0], image_minmax_size[1][0]  # min height  # max height
        ),
    )


def get_random_color():
    # Make sure we don't get a black image
    min_value = 10
    max_value = 256
    return (
        random.randrange(min_value, max_value),  # R
        random.randrange(min_value, max_value),  # G
        random.randrange(min_value, max_value),  # B
        random.randrange(min_value, max_value),  # A
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
    return "{} {} {} {} {} {}\n".format(character, left, bottom, right, top, page)


def generate_image(
    images,
    background_color=(255, 255, 255, 255),
    padding_min_max=PADDING_MIN_MAX,
    space_padding_min_max=SPACE_PADDING_MIN_MAX,
):
    """
    Find the width by summing the width of all the images (and padding)
    Find the height by finding the tallest image of the bunch
    """
    padding = random.randint(padding_min_max[0], padding_min_max[1])
    space_padding = random.randint(space_padding_min_max[0], space_padding_min_max[1])

    background_width = padding * 2
    background_height = 0
    for image in images:
        if image == SPACE_SYMBOL:
            background_width += space_padding
        else:
            background_width += image.size[0] + padding
            if image.size[1] > background_height:
                background_height = image.size[1]
    background_height += padding * 2

    # Intialize the background image
    background_size = (background_width, background_height)
    background = Image.new("RGBA", background_size, background_color)
    x = padding
    y = padding

    # For tesseract, we need to map the coordinates for each symbol
    tesseract_boxes = ""
    for image in images:
        if image == SPACE_SYMBOL:
            x += space_padding
            continue

        width, height = image.size

        # Find ASCII character and map its coordinates
        character = get_symbol_characters([image])
        tesseract_boxes += tesseract_box_string(
            character=character,
            left=x,
            bottom=background_height - y - height,
            right=x + width,
            top=background_height - y,
        )

        # Append the image to the symbol
        offset = (x, y)
        if image.mode == "RGBA":
            # Image is transparent, let's add a mask
            background.paste(image, offset, mask=image)
        else:
            background.paste(image, offset)

        x += width + padding

    return background, tesseract_boxes


# TODO: start using this
def place_images(images, image_minmax_size, background_color=(255, 255, 255)):
    size = get_random_image_size(image_minmax_size)
    print("size={}".format(size), end=", ")

    # White background image
    background = Image.new("RGB", size, (255, 255, 255))

    # Random color to fade into the white background
    background_color = get_random_color()
    print("background_color={}".format(background_color), end=", ")
    foreground = Image.new("RGBA", size, background_color)

    # We now have our base image
    background.paste(foreground, (0, 0), foreground)

    # https://stackoverflow.com/a/54489667
    # and modified for random scale/ratio
    alread_paste_point_list = []
    for img in images:
        # Resize the image/symbol randomly
        seed = random.randint(1, 6)
        width = img.size[0]
        width += random.randint(width - (width // seed), width + (width // seed))
        # To change the 1:1 scale
        # seed = random.randint(1, 6)
        height = img.size[1]
        height += random.randint(height - (height // seed), height + (height // seed))
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

            if all(
                not is_overlap(l1, r1, l2, r2) for l1, r1 in alread_paste_point_list
            ):
                # save alreay pasted points for checking overlap
                alread_paste_point_list.append((l2, r2))
                background.paste(img, (x, y), img)
                break

    return background


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
        (image_count // divider), image_count - (image_count // divider)
    )
    print("symbol_count={}".format(symbol_count), end=", ")

    random.shuffle(images)
    return images[0:symbol_count]


def get_symbols_from_text(symbol_mapping, text):
    symbols = []
    for character in text:
        if not character or character == " ":
            symbols.append(SPACE_SYMBOL)
        else:
            symbols.append(symbol_mapping[character])
    return symbols


def generate_symbol_mapping(images):
    mapping = {}
    for image in images:
        c = chr(int(os.path.basename(image.filename).replace(".png", "")))
        mapping[c] = image

    # Sort the mapping by character and return it
    return collections.OrderedDict(sorted(mapping.items()))


def generate_train_data(
    cipher, wordlist, limit=1000, image_minmax_size=DEFAULT_IMAGE_MINMAX_SIZE
):
    cipher_path = "{}/{}".format(CIPHERS_PATH, cipher)
    cipher_images_path = "{}/images".format(cipher_path)
    train_images_path = "{}/{}".format(TRAIN_DATA_PATH, cipher)
    os.makedirs(train_images_path, exist_ok=True)
    image_paths = sorted(glob.glob("{}/*.png".format(cipher_images_path)))

    # TODO: normalize/clean images for training
    images = [Image.open(path) for path in image_paths]
    image_count = len(images)
    symbol_mapping = generate_symbol_mapping(images)
    print("Cipher image count:", image_count)

    charset = "".join(symbol_mapping.keys())
    print("Cipher charset:", charset)
    digit_count = len(str(limit))

    sentences = generate_sentences(
        charset, wordlist, limit, add_special_sentences=False
    )

    for nr, sentence in enumerate(sentences):
        start_time = time.process_time()
        print('Generating image #{} [sentence="{}"'.format(nr + 1, sentence), end=", ")

        symbols = get_symbols_from_text(symbol_mapping, sentence)

        train_filename = str(nr).zfill(digit_count)  # 0000, 0001, 0002, etc.

        # operation = random.randint(1, 3)
        # TODO: remove, we only use the first operation now
        operation = 1
        print("operation={}".format(operation), end=", ")

        if operation == 1:
            # Combine the symbols into a new image and place it within the original image
            image, tesseract_boxes = generate_image(symbols)

            # TODO: create variants for each image
            # Variants: pixelated, glass, cutout, sprayed, etc.
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

        # Plaintext file for tesseract
        with open("{}/{}.gt.txt".format(train_images_path, train_filename), "w") as f:
            f.write(sentence)

        print("time_taken={}s".format(time.process_time() - start_time), end="]\n")


example_text = """Examples:
# Generate training data with default parameters
generate_train_data.py ancients-stargate-alphabet
# Generate 1000 training data images
generate_train_data.py -l 1000 ancients-stargate-alphabet
# Specify which wordlist to use for generating sentences
generate_train_data.py -w wordlist.txt ancients-stargate-alphabet"""

parser = argparse.ArgumentParser(
    prog="download_images",
    description="Download cipher images from dcode.fr",
    epilog=example_text,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "cipher", help="the name of the cipher to generate training data for"
)
parser.add_argument(
    "-l",
    "--limit",
    type=int,
    default=10000,
    help="how many training data images should be generated",
)
parser.add_argument(
    "-w",
    "--wordlist",
    type=str,
    default="{}/wordlists/languages/british-english-stripped".format(BASE_PATH),
    help="specify the wordlist to use when generating sentences for images",
)

args = parser.parse_args()

# Make sure the cipher exists
cipher = args.cipher
cipher_path = "{}/{}".format(CIPHERS_PATH, cipher)
if not os.path.exists(cipher_path):
    print("[ERROR] Cipher '{}' does not exist ({})".format(cipher, cipher_path))
    exit(1)

# Make sure the wordlist exists
wordlist = args.wordlist
if not os.path.exists(wordlist):
    print("[ERROR] Wordlist does not exist: {}".format(wordlist))
    exit(1)

# Load the wordlist
with open(wordlist) as f:
    wordlist = f.read().splitlines()


limit = args.limit
print("Generating {} training images for cipher:".format(limit), cipher)

generate_train_data(cipher, wordlist, limit=limit)
