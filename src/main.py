import os
import screenshot.screenshot as screenshot
import reader.reader as reader
import camera.camera as camera
from PIL import Image, ImageFilter
import tesserocr
import numpy as np


tess_path = "/opt/homebrew/Cellar/tesseract/5.5.0_1/share/tessdata"

# camera.center_camera()
camera.tech_tree_camera()
img = screenshot.take_screenshot("data/images/ss.png")
print(reader.get_screenshot_text(img))
print(reader.get_screenshot_type(img))
reader.read_screenshot(img, "tech")

camera.tech_info_camera("navigation")
img = screenshot.take_screenshot("data/images/tt.png")

# img = Image.open("data/img10.png")
# with tesserocr.PyTessBaseAPI(path=tess_path, psm=10, oem=3) as api:
#     api.SetVariable("tessedit_char_whitelist", "0123456789")
#     api.SetImage(img)
#     text = api.GetUTF8Text()
# text = text.replace("\n", "")
# print("text:")
# print(text)
# print("end text")