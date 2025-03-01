__version__ = '1.0'

import time
from hidpi_keys import *

HID_DEVICE = "/dev/hidg0"

def char_to_keycode(char):
    """Takes in a character and returns a keycode. The result will always be lowercase"""
    char_lowered = char.lower()
    return KEY_MAPPINGS[char_lowered] if char_lowered in KEY_MAPPINGS else 0x00

def send_key(*keys):
    """Sends key presses, supporting 6 keys at once as well as modifiers (to use multiple modifiers separate them via pipe (|))"""
    report = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for i, key in enumerate(keys):
        if isinstance(key, int):
            report[2 + i] = key
    
    with open(HID_DEVICE, "rb+") as fd:
        fd.write(bytes(report)) 
        fd.write(bytes([0, 0, 0, 0, 0, 0, 0, 0]))

def send_text(text):
    """Sends a string of text, handling lowercase, uppercase, numbers, and special characters"""
    for char in text:
        if char.islower():
            send_key(char_to_keycode(char))
        elif char.isupper():
            send_key(KEY_LEFT_SHIFT, char_to_keycode(char))
        else:
            send_key(char_to_keycode(char))

def send_enter():
    """Sends the Enter key"""
    send_key(KEY_ENTER)

def send_space():
    """Sends the Space key"""
    send_key(KEY_SPACE)

def send_tab():
    """Sends the Tab key"""
    send_key(KEY_TAB)

def send_escape():
    """Sends the Escape key"""
    send_key(KEY_ESC)

def test_hid():
    send_text("abcdefghijklmnopqrstuvwxyz1234567890-=[]\\;',./`~!@#$%^&*()_+{}|:\"<>?")
    send_enter()
