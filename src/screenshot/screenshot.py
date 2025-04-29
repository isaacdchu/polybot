import os
from PIL import Image
from Quartz import (
    CGWindowListCreateImage, kCGWindowListOptionIncludingWindow, kCGNullWindowID, 
    kCGWindowImageBoundsIgnoreFraming, CGWindowListCopyWindowInfo, 
    kCGWindowListOptionOnScreenOnly, CGImageGetWidth, CGImageGetHeight, 
    CGImageGetDataProvider, CGDataProviderCopyData, CGRectInfinite, 
    CGImageGetBytesPerRow
)

def take_screenshot(name: str) -> Image:
    """
    - Description:
    - Takes a screenshot of the game's window (3024px x 1692px)
    - Stores the file in `src/screenshot/data/name.png`
    - Parameters:
        - name: str
            - The name of the file to be stored. Will overwrite if name is already taken
    - Return:
        - A PIL Image object of the screenshot taken
    """
    img = capture_window(get_window_id("Polytopia"))
    box = (0, 132, 3024, 1824)
    img = img.crop(box=box)
    img.save(os.path.join("data", f"{name}.png"))
    return img

def get_window_id(title):
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
    for window in window_list:
        if title.lower() in window.get('kCGWindowName', '').lower():
            return window['kCGWindowNumber']
    return None

def capture_window(window_id):
    image_ref = CGWindowListCreateImage(
        CGRectInfinite,
        kCGWindowListOptionIncludingWindow,
        window_id,
        kCGWindowImageBoundsIgnoreFraming
    )
    if image_ref is None:
        return None

    width = int(CGImageGetWidth(image_ref))
    height = int(CGImageGetHeight(image_ref))
    bytes_per_row = int(CGImageGetBytesPerRow(image_ref))

    data_provider = CGImageGetDataProvider(image_ref)
    data = CGDataProviderCopyData(data_provider)

    img = Image.frombuffer(
        "RGBA",
        (width, height),
        bytes(data),
        "raw",
        "BGRA",
        bytes_per_row,
        1  # orientation
    )
    return img