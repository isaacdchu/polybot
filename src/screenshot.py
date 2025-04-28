import os, sys
from PIL import ImageGrab

def take_screenshot(name: str):
    """Takes a screenshot and saves it to a file."""
    file_path = os.path.join("data", f"{name}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(fp=file_path)
    print(f"Screenshot saved as {file_path}")

# Example usage:
take_screenshot("ss")