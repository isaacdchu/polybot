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


def get_screenshot_text(img: Image) -> str:
    text = pytesseract.image_to_string(img)
    text = text.replace("\n", "")
    return text

def contains_color(img: Image, target_rgb=tuple[int, int, int], tolerance=20):
    img = img.convert('RGB')
    data = np.array(img)
    diff = np.linalg.norm(data - target_rgb, axis=2)
    return np.any(diff <= tolerance)

def get_tech_type(has_tech: bool, locked_tech: bool) -> str:
    if (has_tech == True and locked_tech == True):
        return "owned"
    if (locked_tech == True):
        return "locked"
    return "available"

def filter_tech_image(tech_type: str, img: Image) -> Image:
    box = (0, 36, 99, 69)
    match tech_type:
        case "locked":
            return img
        case "owned":
            return img.crop(box)
        case "available":
            return img.crop(box)

def read_tech(img: Image) -> None:
    def make_full_box(center: tuple[int, int]) -> tuple[int, int, int, int]:
        r = 60
        return (center[0] - r, center[1] - r, center[0] + r, center[1] + r)
    def make_text_box(center: tuple[int, int]) -> tuple[int, int, int, int]:
        w = 50
        h1 = 15
        h2 = 55
        return (center[0] - w, center[1] - h1, center[0] + w, center[1] + h2)
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
    locked_tech_color = (108, 168, 242)
    for i, center in enumerate(centers):
        box = make_text_box(center)
        cropped_img = img.crop(box=box)
        has_tech = contains_color(cropped_img, target_rgb=has_tech_color, tolerance=20)
        locked_tech = not contains_color(cropped_img, target_rgb=locked_tech_color, tolerance=20)
        tech_type = get_tech_type(has_tech, locked_tech)
        filtered_img = filter_tech_image(tech_type, cropped_img)
        text = pytesseract.image_to_string(filtered_img)
        text = text.replace("\n", "")
        filtered_img.save(f"data/node_{i}.png")
        print(f"node: {i:02d} | {text}")