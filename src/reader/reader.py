import os
from PIL import Image
import pytesseract

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
    pass

def get_screenshot_text(img: Image) -> str:
    text = pytesseract.image_to_string(img)
    text = text.replace("\n", "")
    return text