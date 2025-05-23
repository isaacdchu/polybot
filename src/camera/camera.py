import subprocess as subp
import numpy as np
import pyautogui
import time
import json


def center_camera():
    focus_application("Polytopia")
    pyautogui.press("escape")
    pyautogui.press("escape")
    pyautogui.press("2")
    pyautogui.press("2")
    (screen_width, screen_height) = pyautogui.size()
    move_cursor_to_top_right_corner()
    pyautogui.dragTo(0 + 10, 900 - 10, duration=0.15, button="left")
    pyautogui.moveTo(300, 790)
    pyautogui.press("3")
    pyautogui.press("3")
    pyautogui.dragTo(screen_width // 2, screen_height // 2, duration=1, button="left", tween=interpolate_drag)
    time.sleep(0.05)

def tech_tree_camera():
    focus_application("Polytopia")
    pyautogui.press("escape")
    pyautogui.press("escape")
    pyautogui.press("2")
    pyautogui.press("3")
    pyautogui.moveTo(300, 790)

def tech_info_camera(tech_name: str):
    focus_application("Polytopia")
    pyautogui.press("escape")
    pyautogui.press("escape")
    pyautogui.press("2")
    pyautogui.press("2")
    pyautogui.press("3")
    with open("data/game_state/tech_tree.json", "r") as file:
        tech_tree = json.load(file)

    tech_position = tech_tree[tech_name]["center"]
    pyautogui.moveTo(tech_position[0] // 2, (tech_position[1] + 132) // 2)
    pyautogui.click(button="left")
    time.sleep(0.2)

def reset_camera():
    focus_application("Polytopia")
    pyautogui.press("escape")
    pyautogui.press("escape")
    pyautogui.press("2")
    pyautogui.press("2")
    time.sleep(0.1)

def tile_camera(x: int, y: int):
    # check bounds
    if (x < 0 or x > 10 or y < 0 or y > 10):
        print(f"Tile coordinates out of bounds: ({x}, {y})")
        raise IndexError
    focus_application("Polytopia")
    raw_coords = np.array([x, y])
    translation = np.array([1487, 1345])
    transformation = np.array([[83.529412, -83.6765], [-48.470588, -50.6765]])
    coords = np.matmul(transformation, raw_coords.T) + translation
    coords = coords.astype(int)
    # rescale to screen size, which has half the resolution on x and y
    coords[0] = (coords[0] >> 1) + 3
    coords[1] = (coords[1] >> 1) + 66
    pyautogui.moveTo(coords[0], coords[1])

def focus_application(app_name):
    try:
        # Use AppleScript to bring the application to the front
        script = f'''
        tell application "{app_name}"
            activate
        end tell
        '''
        subp.run(["osascript", "-e", script], check=True)
    except subp.CalledProcessError as e:
        print(f"Failed to focus on application: {app_name}. Error: {e}")
        raise RuntimeError

def move_cursor_to_center():
    (screen_width, screen_height) = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    pyautogui.moveTo(center_x, center_y)

def move_cursor_to_top_right_corner():
    (screen_width, screen_height) = pyautogui.size()
    pyautogui.moveTo(screen_width - 10, 66 + 10)

def interpolate_drag(t: float) -> float:
    # t is from 0.0 to 1.0
    # moves slow at beginning, fast in middle, then holds for last quarter
    if (t > 0.5):
        return 1
    return 4 * (t ** 2)