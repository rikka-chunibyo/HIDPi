import time
from hidpi import Keyboard, Mouse
from hidpi.keyboard_keys import *
from hidpi.mouse_buttons import *

def test_keyboard():
    print("Testing keyboard...")
    Keyboard.send_text("Hello, HIDPi!")
    time.sleep(1)
    Keyboard.hold_key(KEY_ENTER)
    time.sleep(3)
    Keyboard.release_keys()
    time.sleep(1)

def test_mouse():
    print("Testing mouse...")
    Mouse.move(50, 50)
    time.sleep(1)
    Mouse.click(LEFT)
    time.sleep(1)
    Mouse.move(-50, -50)
    time.sleep(1)

if __name__ == "__main__":
    test_keyboard()
    test_mouse()
    print("Tested")
