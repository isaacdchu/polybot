from PIL import Image
from math import ceil
import tesserocr
import numpy as np

tess_path = "/opt/homebrew/Cellar/tesseract/5.5.0_1/share/tessdata"

all_tile_types = {
        "animal": "field",
        "bridge": "bridge",
        "port": "port",
        "fish": "",
        "starfish": "",
        "water": "water",
        "ocean": "ocean",
        "lighthouse": "unknown",
        "forest": "field",
        "crop": "field",
        "village": "field",
        "mountain": "mountain",
        "farm": "field",
        "market": "field",
        "windmill": "field",
        "lumber hut": "field",
        "sawmill": "field",
        "mine": "moutnain",
        "forge": "field",
        "ruin": "unknown",
        "city": "field",
        "road": "road",
        "forest temple": "field",
        "water temple": "unknown",
        "mountain temple": "mountain",
        "temple": "field"
    }

all_unit_types = {
    "enemy": "",
    "warrior": "",
    "rider": "",
    "archer": "",
    "defender": "",
    "mind bender": "",
    "cloak": "",
    "catapult": "",
    "knight": "",
    "giant": "",
    "raft": "",
    "rammer": "",
    "scout": "",
    "bomber": ""
}

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

def get_screenshot_text(img: Image) -> str:
    img = img.convert("RGB")
    with tesserocr.PyTessBaseAPI(path=tess_path) as api:
        api.SetImage(img)
        text = api.GetUTF8Text()
    text = text.replace("\n", " ")
    return text

def contains_color(img: Image, target_rgb=tuple[int, int, int], tolerance=20) -> bool:
    img = img.convert('RGB')
    data = np.array(img)
    diff = np.linalg.norm(data - target_rgb, axis=2)
    return np.any(diff <= tolerance)

def calc_tech_cost(k: list[dict]) -> list[dict]:
    # cost of tech = (tier * cities + 4)
    # literacy = ceil(2 * cost / 3)
    def find_num_cities(has_literacy: bool) -> int:
        with tesserocr.PyTessBaseAPI(path=tess_path, psm=10, oem=3) as api:
            box = (1709, 724, 1738, 742)
            img = Image.open("data/images/tech_tree/tt.png").crop(box=box).convert("RGB")
            api.SetVariable("tessedit_char_whitelist", "0123456789")
            api.SetImage(img)
            # img.save("data/test.png")
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