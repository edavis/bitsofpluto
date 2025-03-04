#!/usr/bin/env python
"""
Bluesky bot posting a different bit of Pluto every six hours.
Photo by NASA's New Horizons spacecraft.
https://www.nasa.gov/image-feature/the-rich-color-variations-of-pluto/
"""
import os
import argparse
import random
from io import BytesIO
from PIL import Image
from atproto import Client, models

WIDTHS = [600, 800, 1000, 1200, 2000]
BSKY_PDS_HOST = os.getenv('BSKY_PDS_HOST')
BSKY_HANDLE = os.getenv('BSKY_HANDLE')
BSKY_APP_PASSWORD = os.getenv('BSKY_APP_PASSWORD')

def crop_is_bright_enough(cropped):
    top, right, bottom, left = 0, cropped.width - 1, cropped.height - 1, 0
    points = [
        (left, top),
        (right, top),
        (right / 2, top),
        (left, bottom / 2),
        (right, bottom / 2),
        (right / 2, bottom / 2),
        (left, bottom),
        (right, bottom),
        (right / 2, bottom),
    ]
    total_dark_points = 0

    for point in points:
        r, g, b = cropped.getpixel(point)
        brightness = sum([r, g, b]) / 3  # 0 is black and 255 is white
        if brightness < 10:
            total_dark_points += 1

    return total_dark_points <= 6


def crop_image(pluto_filename: str) -> str:
    """Get a bit of Pluto"""
    pluto = Image.open(pluto_filename)
    while True:
        width = random.choice(WIDTHS)
        height = width * 0.75
        x = random.randrange(0, int(pluto.width - width + 1))
        y = random.randrange(0, int(pluto.height - height + 1))
        bit_of_pluto = pluto.crop((x, y, x + width, y + height))
        if crop_is_bright_enough(bit_of_pluto):
            break

    buf = BytesIO()
    bit_of_pluto.save(buf, 'JPEG', quality=95)
    return buf, width, height


def send_post(args):
    client = Client(BSKY_PDS_HOST)
    client.login(BSKY_HANDLE, BSKY_APP_PASSWORD)

    cropped, width, height = crop_image(args.pluto)
    client.send_image(
        text = '',
        image = cropped,
        image_alt = "A cropped image of Pluto taken by NASA's New Horizons spacecraft.",
        image_aspect_ratio = models.AppBskyEmbedDefs.AspectRatio(width=width, height=height)
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Posting a different bit of Pluto every six hours.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", "--pluto", default="crop_p_color2_enhanced_release.png", help="Path to a big photo of Pluto")
    args = parser.parse_args()
    send_post(args)

if __name__ == "__main__":
    main()
