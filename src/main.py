import os
import screenshot.screenshot as screenshot
import reader.reader as reader
import camera.camera as camera
from PIL import ImageFilter
from PIL import ImageEnhance

camera.center_camera()
img = screenshot.take_screenshot("ss")
print(reader.get_screenshot_text(img))
print(reader.get_screenshot_type(img))