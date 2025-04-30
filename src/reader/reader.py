import os
from PIL import Image
import pytesseract
import numpy as np

def get_screenshot_type(img: Image) -> str:
    text = get_screenshot_text(img).lower()
    keywords = {
        "costs increase for": "tech",
        "(v]": "info",
        "settings": "game"
    }
    for key, value in keywords.items():
        if key in text:
            return value
    return "none"

def read_screenshot(img: Image, type: str) -> None:
    if (type == "tech"):
        read_tech(img)
        return


def get_screenshot_text(img: Image) -> str:
    text = pytesseract.image_to_string(img)
    text = text.replace("\n", "")
    return text

def contains_color(img: Image, target_rgb=tuple[int, int, int], tolerance=20):
    img = img.convert('RGB')
    data = np.array(img)
    diff = np.linalg.norm(data - target_rgb, axis=2)
    return np.any(diff <= tolerance)

def read_tech(img: Image) -> None:
    def make_box(center: tuple[int, int]) -> tuple[int, int, int, int]:
        r = 60
        return (center[0] - r, center[1] -r, center[0] + r, center[1] + r)
    centers = [
        (1583, 686),
        (1697, 849),
        (1579, 1009),
        (1388, 944),
        (1391, 741),
        (1533, 522)
    ]
    has_tech_color = (130, 207, 113)
    for i, center in enumerate(centers):
        box = make_box(center)
        cropped_img = img.crop(box=box)
        text = pytesseract.image_to_string(cropped_img)
        has_tech = contains_color(cropped_img, target_rgb=has_tech_color, tolerance=20)
        # if (has_tech == True):
            # add to tech upgraded

        # TODO else: check for blue for available upgrade, then if no blue, add to locked tech
        cropped_img.save(f"data/node_{i}.png")
        print(text)
