import os
from PIL import Image
from Quartz import (
    CGWindowListCreateImage, kCGWindowListOptionIncludingWindow, kCGNullWindowID, 
    kCGWindowImageBoundsIgnoreFraming, CGWindowListCopyWindowInfo, 
    kCGWindowListOptionOnScreenOnly, CGImageGetWidth, CGImageGetHeight, 
    CGImageGetDataProvider, CGDataProviderCopyData, CGRectInfinite, 
    CGImageGetBytesPerRow
)

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

# Usage
title = 'Polytopia'
window_id = get_window_id(title)
if window_id:
    img = capture_window(window_id)
    if img:
        img.save(os.path.join("data", "ss.png"))
    else:
        print('Failed to capture window.')
else:
    print('Window not found.')