#!/usr/bin/python
import glob
import math
import os
import pathlib

from PIL import Image, ImageDraw

# White background
BACKGROUND_COLOR = (255, 255, 255)

# Images per row
IMAGES_PER_ROW = 20

# How many pixels should we pad between the images?
PADDING_PIXELS = 10

# Adds an intial padding before placing images
INITIAL_PADDING = True

# Draw grid?
# We draw both, see bottom of the script
# DRAW_GRID = True
GRID_LINE_COLOR = (230, 230, 230)
GRID_LINE_WIDTH = 0.5

#############################################################################

BASE_PATH = pathlib.Path(__file__).resolve().parents[1].absolute()
CIPHERS_PATH = "{}/ciphers".format(BASE_PATH)
CIPHERS = sorted(next(os.walk(CIPHERS_PATH))[1])

#############################################################################


def generate_combined_image(
    image_paths,
    images_per_row,
    background_color,
    padding_pixels,
    add_initial_padding,
    draw_grid,
    grid_line_width,
    grid_line_color,
):
    image_count = len(image_paths)
    expected_row_count = math.ceil(image_count / images_per_row)

    # Are all the image sizes identical? (and load the images into a list)
    identical = True
    images = []
    last_size = None
    for image_path in image_paths:
        image = Image.open(image_path)
        images.append(image)
        if last_size is not None and last_size != image.size:
            identical = False
        last_size = image.size

    if identical:
        # Get the size (width, height) of the images (they are identical),
        image_size = images[0].size
        image_width = image_size[0]
        image_final_width = image_width + (padding_pixels * 2)
        image_height = image_size[1]
        image_final_height = image_height + (padding_pixels * 2)

        # Calculate the image width and handle the extra padding
        combined_width = image_final_width * images_per_row
        combined_width += (padding_pixels * 2) if add_initial_padding else 0

        # Calculate the image height and handle the extra padding
        combined_height = image_final_height * expected_row_count
        combined_height += (padding_pixels * 2) if add_initial_padding else 0
    else:
        """
        The sizes are different, we need to loop through the images
        and calculate the width and height by checking each image per row.
        """
        x, y = 0, 0
        rows = []
        row_width = 0
        row_height = 0
        for image_index, image in enumerate(images):
            x += image.size[0]

            if image.size[1] > row_height:
                # We have a image that's taller than another image in the row
                row_height = image.size[1]

            # Increase the row width
            row_width += image.size[0]

            if image_index > 0 and image_index % images_per_row == 0:
                # New row, reset variables
                x = 0
                rows.append((row_width, row_height))
                row_width = 0
                row_height = 0

        # Add the last row if missing
        if expected_row_count != len(rows):
            rows.append((row_width, row_height))

        # Find widest row and add padding
        combined_width = max([row[0] for row in rows])
        combined_width += padding_pixels * ((images_per_row * 2) - 1)
        combined_width += padding_pixels if add_initial_padding else 0

        # Sum the height of the rows and add padding
        combined_height = sum([row[1] for row in rows])
        # combined_height += (padding_pixels * (len(rows) + (1 if add_initial_padding else 0)))
        combined_height += padding_pixels * (len(rows) * 2)
        combined_height += padding_pixels if add_initial_padding else 0

    # Create the initial image with white background
    combined = Image.new("RGB", (combined_width, combined_height), background_color)

    # Initial positioning
    reset_x = padding_pixels if add_initial_padding else 0
    reset_y = padding_pixels if add_initial_padding else 0

    reset_x += padding_pixels
    reset_y += padding_pixels

    x, y = reset_x, reset_y

    x_end = combined.size[0] - (padding_pixels if add_initial_padding else 0)
    y_end = combined.size[1] - (padding_pixels if add_initial_padding else 0)

    # Loop through all the images and add them to the combined image
    row_index = 0

    for i, image in enumerate(images):
        image_index = i + 1
        combined.paste(image, (x, y), mask=image.convert("RGBA"))

        # New row
        if identical:
            row_height = image_final_height
        else:
            row_height = rows[row_index][1] + (padding_pixels * 2)

        is_last_row = (row_index + 1) == expected_row_count
        is_new_row = image_index != 1 and image_index % images_per_row == 0

        # Add vertical grid line?
        if draw_grid and x != reset_x:
            # Find the x position between the rows and add a line there
            line_x = x - padding_pixels - (grid_line_width / 2)
            line_y_end = row_height

            if row_index == 0 or is_last_row:
                if is_last_row:
                    line_y_start = y - padding_pixels
                    line_y_end = y_end
                else:
                    line_y_start = padding_pixels if add_initial_padding else 0
                    line_y_end += padding_pixels if add_initial_padding else 0
            else:
                line_y_start = y - padding_pixels
                line_y_end += line_y_start

            draw = ImageDraw.Draw(combined)
            draw.rectangle(
                [(line_x, line_y_start), (line_x + grid_line_width, line_y_end)],
                fill=grid_line_color,
            )

        """
        # Add the last vertical line to each row?
        if is_last_image or is_last_image_of_row:
            # Add the last vertical line
            line_x += image_final_width if identical else (image.size[0] + (padding_pixels * 2))
            draw = ImageDraw.Draw(combined)
            draw.rectangle([
                    (line_x, line_y_start),
                    (line_x + grid_line_width, line_y_end)
                ],
                fill=grid_line_color
            )
        """

        if not is_new_row:
            # Just increase the current x position
            x += (
                image_final_width
                if identical
                else (image.size[0] + (padding_pixels * 2))
            )
        else:
            # New row
            x = reset_x
            y += row_height

            # Add horizontal grid line?
            if draw_grid and not is_last_row:
                # Find the y position between the rows and add a line there
                line_x = padding_pixels if add_initial_padding else 0
                line_y = y - padding_pixels - (grid_line_width / 2)
                draw = ImageDraw.Draw(combined)
                draw.rectangle(
                    [(line_x, line_y), (x_end, line_y + grid_line_width)],
                    fill=grid_line_color,
                )

            row_index += 1

    return combined


for cipher in CIPHERS:
    print("Generating combined images for cipher:", cipher)
    cipher_path = "{}/{}".format(CIPHERS_PATH, cipher)
    cipher_images_path = "{}/images".format(cipher_path)
    image_paths = sorted(glob.glob("{}/*.png".format(cipher_images_path)))

    for draw_grid in (True, False):
        combined_image = generate_combined_image(
            image_paths=image_paths,
            images_per_row=IMAGES_PER_ROW,
            background_color=BACKGROUND_COLOR,
            padding_pixels=PADDING_PIXELS,
            add_initial_padding=INITIAL_PADDING,
            draw_grid=draw_grid,
            grid_line_width=GRID_LINE_WIDTH,
            grid_line_color=GRID_LINE_COLOR,
        )
        combined_path = "{}/combined{}.png".format(
            cipher_path, "_grid" if draw_grid else ""
        )
        combined_image.save(combined_path, "PNG")
