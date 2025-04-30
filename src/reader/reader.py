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
        # Tier 1: Riding -> Hunting
        (1582, 685),
        (1697, 849),
        (1579, 1009),
        (1388, 944),
        (1391, 741),

        # Tier 2: Roads -> Forestry
        (1533, 522),
        (1721, 587),
        (1836, 752),
        (1833, 952),
        (1712, 1114),
        (1520, 1171),
        (1330, 1106),
        (1216, 941),
        (1220, 741),
        (1340, 580),

        #Tier 3: Trade -> Mathematics
        (1481, 359),
        (1861, 490),
        (1976, 654),
        (1968, 1055),
        (1848, 1215),
        (1465, 1332),
        (1273, 1266),
        (1045, 938),
        (1048, 738),
        (1290, 418)
    ]
    has_tech_color = (130, 207, 113)
    for i, center in enumerate(centers):
        box = make_box(center)
        cropped_img = img.crop(box=box)
        # TODO need more preprocessing before converting to string
        text = pytesseract.image_to_string(cropped_img)
        has_tech = contains_color(cropped_img, target_rgb=has_tech_color, tolerance=20)
        # if (has_tech == True):
            # add to tech upgraded

        # TODO else: check for blue for available upgrade, then if no blue, add to locked tech
        cropped_img.save(f"data/node_{i}.png")
        print(text)
