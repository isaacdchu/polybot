import subprocess as subp
import pyautogui
import time

def center_camera():
    focus_application("Polytopia")
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
    pyautogui.press("2")
    pyautogui.press("3")
    pyautogui.moveTo(300, 790)

def focus_application(app_name):
    try:
        # Use AppleScript to bring the application to the front
        script = f'''
        tell application "{app_name}"
            activate
        end tell
        '''
        subp.run(["osascript", "-e", script], check=True)
        print(f"Focused on application: {app_name}")
    except subp.CalledProcessError as e:
        print(f"Failed to focus on application: {app_name}. Error: {e}")

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