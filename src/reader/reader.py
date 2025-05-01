import os
from PIL import Image
import tesserocr
import numpy as np

tess_path = "/opt/homebrew/Cellar/tesseract/5.5.0_1/share/tessdata"

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
    match type:
        case "tech":
            read_tech(img)
        case "info":
            return
        case "game":
            return

def get_screenshot_text(img: Image) -> str:
    img = img.convert("RGB")
    with tesserocr.PyTessBaseAPI(path=tess_path) as api:
        api.SetImage(img)
        text = api.GetUTF8Text()
    text = text.replace("\n", "")
    return text

def contains_color(img: Image, target_rgb=tuple[int, int, int], tolerance=20):
    img = img.convert('RGB')
    data = np.array(img)
    diff = np.linalg.norm(data - target_rgb, axis=2)
    return np.any(diff <= tolerance)

def read_tech(img: Image) -> None:
    def make_full_box(center: tuple[int, int]) -> tuple[int, int, int, int]:
        r = 60
        return (center[0] - r, center[1] - r, center[0] + r, center[1] + r)
    
    def filter_for_red(img: Image) -> Image:
        img = img.convert("RGB")
        data = np.array(img)
        mask = (data[..., 0] >= 120) & (data[..., 1] < 110) & (data[..., 2] < 110)
        data[mask] = [0, 0, 0]  # Black
        data[~mask] = [255, 255, 255]  # White
        return Image.fromarray(data)
    
    def filter_for_white(img: Image) -> Image:
        img = img.convert("RGB")
        data = np.array(img)
        mask = (data[..., 0] > 150) & (data[..., 1] > 160) & (data[..., 2] > 170)
        data[mask] = [0, 0, 0]  # Black
        data[~mask] = [255, 255, 255]  # White
        return Image.fromarray(data)

    def get_tech_type(has_tech: bool, locked_tech: bool) -> str:
        if (has_tech == True):
            return "owned"
        if (locked_tech == True):
            return "locked"
        return "available"

    def filter_tech_image(tech_type: str, img: Image) -> Image:
        box = (0, 76, 99, 103)
        match tech_type:
            case "locked":
                return img
            case "owned":
                return img.crop(box)
            case "available":
                return img.crop(box)
    
    def get_tech_cost(img: Image, counter: int) -> str:
        box = (0, 0, 99, 22)
        img = img.crop(box)
        # if there is red
        img = filter_for_red(img) if contains_color(img, (190, 91, 65), 15) else filter_for_white(img)
        img.save(f"data/img{counter}.png")
        with tesserocr.PyTessBaseAPI(path=tess_path) as api:
            api.SetImage(img)
            text = api.GetUTF8Text()
        return text

    def make_text_box(center: tuple[int, int]) -> tuple[int, int, int, int]:
        w = 50
        h1 = 55
        h2 = 50
        return (center[0] - w, center[1] - h1, center[0] + w, center[1] + h2)
    centers = [
        # Tier 1: Riding -> Hunting
        (1582, 683),
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
        filtered_img = filter_tech_image(tech_type, cropped_img).convert("RGB")
        with tesserocr.PyTessBaseAPI(path=tess_path) as api:
            api.SetImage(filtered_img)
            text = api.GetUTF8Text()
        text = text.replace("\n", "")
        filtered_img.save(f"data/images/tech_tree/node_{i}.png")
        cost = "."
        if (tech_type == "available"):
            cost = get_tech_cost(cropped_img, i)
        print(f"node: {i:02d} | {text} | {tech_type} | {cost}")