import os
import screenshot.screenshot as screenshot
import reader.reader as reader
import camera.camera as camera
from PIL import Image, ImageFilter
import tesserocr
import numpy as np
import pyautogui
import json
import time

tess_path = "/opt/homebrew/Cellar/tesseract/5.5.0_1/share/tessdata"

camera.center_camera()
tiles = {}
for i in range(0, 11):
    for j in range(0, 11):
        camera.tile_camera(i, j)
        pyautogui.click(button="left")
        time.sleep(0.1)
        img = screenshot.take_screenshot("data/images/game/ss.png")
        if (reader.detect_unit(img) == True):
            pyautogui.click(button="left")
            time.sleep(0.1)
            img = screenshot.take_screenshot("data/images/game/ss.png")
        tile = reader.read_screenshot(img, "info")
        tiles[f"{i}, {j}"] = tile
        pyautogui.press("2")
        pyautogui.press("2")
with open("data/game_state/tiles.json", "w") as file:
    json.dump(tiles, file, indent=4)

# camera.center_camera()
# img = screenshot.take_screenshot("data/images/game/ss.png")
# img = Image.open("data/images/game/ss.png")
# img_type = reader.get_screenshot_type(img)
# print(reader.get_screenshot_text(img))
# print(img_type)
# reader.read_screenshot(img, img_type)

# camera.tech_tree_camera()
# img = screenshot.take_screenshot("data/images/tech_tree/ss.png")
# camera.tech_info_camera("navigation")
# screenshot.take_screenshot("data/images/tech_tree/tt.png")
# print(reader.get_screenshot_text(img))
# print(reader.get_screenshot_type(img))
# reader.read_screenshot(img, "tech")

# img = Image.open("data/img10.png")
# with tesserocr.PyTessBaseAPI(path=tess_path, psm=10, oem=3) as api:
#     api.SetVariable("tessedit_char_whitelist", "0123456789")
#     api.SetImage(img)
#     text = api.GetUTF8Text()
# text = text.replace("\n", "")
# print("text:")
# print(text)
# print("end text")