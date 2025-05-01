import os
from PIL import Image, ImageFilter
import tesserocr
import numpy as np
from math import ceil
import json


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
            tech_dict = read_tech(img)
            rel_output_path = os.path.join("data", "game_state", "tech_tree.json")
            abs_output_path = os.path.realpath(rel_output_path)
            with open(abs_output_path, "w") as f:
                json.dump(tech_dict, f, indent=4)
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

def read_tech(img: Image) -> dict:
    # array for going from index to name
    tech_name_map = [
        "riding",
        "organization",
        "climbing",
        "fishing",
        "hunting",
        "roads",
        "free_spirit",
        "farming",
        "strategy",
        "mining",
        "meditation",
        "sailing",
        "ramming",
        "archery",
        "forestry",
        "trade",
        "chivalry",
        "construction",
        "diplomacy",
        "smithery",
        "philosophy",
        "navigation",
        "aquatism",
        "spiritualism",
        "mathematics"
    ]

    def make_full_box(center: tuple[int, int]) -> tuple[int, int, int, int]:
        r = 60
        return (center[0] - r, center[1] - r, center[0] + r, center[1] + r)
    
    def calc_tech_cost(k: list[dict]) -> list[dict]:
        # cost of tech = (tier * cities + 4)
        # literacy = ceil(cost / 3)
        def find_num_cities(has_literacy: bool, k: list[dict]) -> int:
            city_data = []
            for i, item in enumerate(k):
                if (item["cost"] > 0):
                    cost = (item["cost"] - 4) / get_tech_tier(i)
                    if (has_literacy == True):
                        cost = ceil(cost / 3)
                    city_data.append(int(cost))
            most_common = max(set(city_data), key=city_data.count)
            return most_common

        has_literacy = False
        if (k[20]["status"] == "owned"):
            has_literacy = True

        num_cities = find_num_cities(has_literacy, k)
        for i in range(len(k)):
            cost = get_tech_tier(i) * num_cities + 4
            if (has_literacy == True):
                cost = ceil(cost / 3)
            k[i]["cost"] = cost
        return k

    def get_tech_type(has_tech: bool, locked_tech: bool) -> str:
        if (has_tech == True):
            return "owned"
        if (locked_tech == True):
            return "locked"
        return "available"
    
    def get_tech_tier(index: int) -> int:
        if (index <= 4):
            return 1
        if (index <= 14):
            return 2
        return 3
    
    def get_tech_cost(img: Image, counter: int) -> int:
        def filter_for_red(img: Image) -> Image:
            img = img.convert("RGB")
            data = np.array(img)
            mask = (data[..., 0] >= 110) & (data[..., 1] < 110) & (data[..., 2] < 110)
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
        
        def upscale_image(img: Image) -> Image:
            arr = np.array(img)
            # Upscale: 3x by repeating pixels
            scale_factor = 3
            upscaled_arr = arr.repeat(scale_factor, axis=0).repeat(scale_factor, axis=1)
            upscaled_img = Image.fromarray(upscaled_arr)

            # Apply slight Gaussian blur
            blurred_img = upscaled_img.filter(ImageFilter.GaussianBlur(radius=1))

            # Create a white background (500x150)
            background = Image.new("L", (500, 150), color=255)

            # Calculate top-left corner to paste the image centered
            bg_w, bg_h = background.size
            img_w, img_h = blurred_img.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

            # Paste the blurred image onto the background
            background.paste(blurred_img, offset)
            return background
        
        # if there is red, use filter for red, else use filter for white
        img = filter_for_red(img) if contains_color(img, (190, 91, 65), 15) else filter_for_white(img)
        img = upscale_image(img)
        img.save(f"data/img{counter}.png")
        with tesserocr.PyTessBaseAPI(path=tess_path, psm=10, oem=3) as api:
            api.SetVariable("tessedit_char_whitelist", "0123456789")
            api.SetImage(img)
            text = api.GetUTF8Text()
        text.replace("\n", "").strip()
        if (len(text) == 0):
            return 0
        return int(text)

    def make_cost_box(center: tuple[int, int]) -> tuple[int, int, int, int]:
        w = 40
        h1 = 55
        h2 = -30
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
    tech_data = []
    for i, center in enumerate(centers):
        box = make_cost_box(center)
        cropped_img = img.crop(box=box)
        has_tech = contains_color(cropped_img, target_rgb=has_tech_color, tolerance=20)
        locked_tech = not contains_color(cropped_img, target_rgb=locked_tech_color, tolerance=20)
        tech_type = get_tech_type(has_tech, locked_tech)
        cost = 0
        if (tech_type == "available"):
            cost = get_tech_cost(cropped_img, i)
        cropped_img.save(f"data/images/tech_tree/node_{i}.png")
        # print(f"node: {i:02d} | {tech_type} | {cost} | {get_tech_tier(i)}")
        tech_data.append({"status": tech_type, "cost": cost})
    
    tech_data = calc_tech_cost(tech_data)
    tech_dict = {}
    for i, tech_name in enumerate(tech_name_map):
        tech_dict[tech_name] = tech_data[i]
    return tech_dict