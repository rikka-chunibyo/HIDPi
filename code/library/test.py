import time
import math

from hidpi import Keyboard, Mouse
from hidpi.keyboard_keys import *
from hidpi.mouse_buttons import *

def test_keyboard():
    print("Testing keyboard...")
    time.sleep(1)
    Keyboard.send_text("Hello, HIDPi!")
    time.sleep(1)
    Keyboard.hold_key(0, KEY_A)
    time.sleep(1)
    Keyboard.release_keys()
    time.sleep(1)

def test_mouse():
    print("Testing mouse...")
    time.sleep(1)
    
    radius = 5
    
    for angle in range(0, 360, 1):
        x = int(radius * math.cos(math.radians(angle)))
        y = int(radius * math.sin(math.radians(angle)))
        Mouse.move(x, y)
        time.sleep(0.01)

if __name__ == "__main__":
    test_keyboard()
    test_mouse()
    print("Tested")
