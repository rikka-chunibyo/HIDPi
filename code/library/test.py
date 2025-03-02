import time
from hidpi import *

def test_keyboard():
    print("Testing keyboard...")
    Keyboard.send_text("Hello, HIDPi!")
    time.sleep(1)
    Keyboard.send_key(KEY_ENTER)
    time.sleep(1)

def test_mouse():
    print("Testing mouse...")
    Mouse.move(50, 50)
    time.sleep(1)
    Mouse.click(1)
    time.sleep(1)
    Mouse.move(-50, -50)
    time.sleep(1)

if __name__ == "__main__":
    test_keyboard()
    test_mouse()
    print("Tested")
