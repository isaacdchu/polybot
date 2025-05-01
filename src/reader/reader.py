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
        "[v)": "info",
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
            read_info(img)
        case "game":
            return

def get_screenshot_text(img: Image) -> str:
    img = img.convert("RGB")
    with tesserocr.PyTessBaseAPI(path=tess_path) as api:
        api.SetImage(img)
        text = api.GetUTF8Text()
    text = text.replace("\n", "")
    return text

def contains_color(img: Image, target_rgb=tuple[int, int, int], tolerance=20) -> bool:
    img = img.convert('RGB')
    data = np.array(img)
    diff = np.linalg.norm(data - target_rgb, axis=2)
    return np.any(diff <= tolerance)

def read_info(img: Image) -> dict:
    box = (146, 1530, 482, 1637)
    img = img.crop(box=box)
    img.save("data/images/game/info.png")
    print(get_screenshot_text(img))
    return {}

def read_tech(img: Image) -> dict:
    def calc_tech_cost(k: list[dict]) -> list[dict]:
        # cost of tech = (tier * cities + 4)
        # literacy = ceil(2 * cost / 3)
        def find_num_cities(has_literacy: bool) -> int:
            with tesserocr.PyTessBaseAPI(path=tess_path, psm=10, oem=3) as api:
                box = (1702, 687, 1738, 705)
                img = Image.open("data/images/tech_tree/tt.png").crop(box=box).convert("RGB")
                api.SetVariable("tessedit_char_whitelist", "0123456789")
                api.SetImage(img)
                img.save("data/test.png")
                tier_3_cost = int(api.GetUTF8Text().replace("\n", "").strip())
                print(tier_3_cost)
            if (has_literacy == True):
                num_cities = (1.5 * tier_3_cost - 4) // 3
            else:
                num_cities = (tier_3_cost - 4) // 3
            return int(num_cities)

        has_literacy = False
        if (k[20]["status"] == "owned"):
            has_literacy = True

        num_cities = find_num_cities(has_literacy)
        for i in range(len(k)):
            cost = get_tech_tier(i) * num_cities + 4
            if (has_literacy == True):
                cost = ceil(2 * cost / 3)
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

    def make_sample_box(center: tuple[int, int]) -> tuple[int, int, int, int]:
        w = 40
        h1 = 55
        h2 = -30
        return (center[0] - w, center[1] - h1, center[0] + w, center[1] + h2)
    
    with open("data/game_state/tech_tree.json", "r") as f:
        data = json.load(f)
        centers = [data[item]["center"] for item in data]
        tech_names = [item for item in data]

    has_tech_color = (130, 207, 113)
    locked_tech_color = (108, 168, 242)
    tech_data = []
    for i, center in enumerate(centers):
        box = make_sample_box(center)
        cropped_img = img.crop(box=box)
        has_tech = contains_color(cropped_img, target_rgb=has_tech_color, tolerance=20)
        locked_tech = not contains_color(cropped_img, target_rgb=locked_tech_color, tolerance=20)
        tech_type = get_tech_type(has_tech, locked_tech)
        # print(f"node: {i:02d} | {tech_type} | {cost} | {get_tech_tier(i)}")
        tech_data.append({"status": tech_type, "cost": 0, "center": centers[i]})
    
    tech_data = calc_tech_cost(tech_data)
    tech_dict = {}
    for i, tech_name in enumerate(tech_names):
        tech_dict[tech_name] = tech_data[i]
    return tech_dict