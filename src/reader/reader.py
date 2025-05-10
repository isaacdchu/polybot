import os
from PIL import Image
import json
import reader.reader_utilities as utils

def read_screenshot(img: Image, type: str = None) -> dict:
    img_type = utils.get_screenshot_type(img) if type == None else type
    match img_type:
        case "tech":
            tech_dict = read_tech(img)
            rel_output_path = os.path.join("data", "game_state", "tech_tree.json")
            abs_output_path = os.path.realpath(rel_output_path)
            with open(abs_output_path, "w") as f:
                json.dump(tech_dict, f, indent=4)
            return tech_dict
        case "info":
            return read_info(img)
        case "game":
            return {}

def read_info(img: Image) -> dict:
    box = (146, 1530, 482, 1637)
    img = img.crop(box=box)
    # img.save("data/images/game/info.png")
    text = utils.get_screenshot_text(img).lower()
    attributes = []
    travel_type = "default"
    for key, value in utils.all_tile_types.items():
        if key in text:
            if (key == "city" and len(attributes) > 0 ):
                continue
            if (key == "road" and ("city" in attributes)):
                continue
            attributes.append(key)
            if (travel_type != "unknown"):
                travel_type = value
    if (travel_type == "default"):
        travel_type = "unknown"
    # fog of war if nothing matches
    if (len(attributes) == 0):
        attributes.append("fow")
        travel_type = "fow"
    # correct for "city" being in descriptions of non-city tiles
    if ("city" in attributes and len(attributes) > 1):
        attributes.remove("city")
    return {"attributes": attributes, "travel_type": travel_type}

def detect_unit(img: Image) -> bool:
    # returns true if there is a unit on the tile
    text = utils.get_screenshot_text(img).lower()
    for key, _ in utils.all_unit_types.items():
        if (key in text):
            return True
    return False

def read_tech(img: Image) -> dict:
    with open("data/game_state/tech_tree.json", "r") as f:
        data = json.load(f)
        centers = [data[item]["center"] for item in data]
        tech_names = [item for item in data]

    has_tech_color = (130, 207, 113)
    locked_tech_color = (108, 168, 242)
    tech_data = []
    for i, center in enumerate(centers):
        box = utils.make_sample_box(center)
        cropped_img = img.crop(box=box)
        has_tech = utils.contains_color(cropped_img, target_rgb=has_tech_color, tolerance=20)
        locked_tech = not utils.contains_color(cropped_img, target_rgb=locked_tech_color, tolerance=20)
        tech_type = utils.get_tech_type(has_tech, locked_tech)
        # print(f"node: {i:02d} | {tech_type} | {cost} | {get_tech_tier(i)}")
        tech_data.append({"status": tech_type, "cost": 0, "center": centers[i]})
    
    tech_data = utils.calc_tech_cost(tech_data)
    tech_dict = {}
    for i, tech_name in enumerate(tech_names):
        tech_dict[tech_name] = tech_data[i]
    return tech_dict