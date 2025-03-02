__version__ = '1.1'

import time
from hidpi_keys import *

HID_DEVICE = "/dev/hidg0"

# UTiLiTY FUNCTiONS
def char_to_keycode(char):
    """Takes in a character and returns a keycode. The result will always be lowercase"""
    char_lowered = char.lower()
    return KEY_MAPPINGS[char_lowered] if char_lowered in KEY_MAPPINGS else 0x00

def test_hid():
    send_text("abcdefghijklmnopqrstuvwxyz1234567890-=[]\\;',./`~!@#$%^&*()_+{}|:\"<>?")

# KEY REPORT FUNCTiONS
def send_key(*keys, delay=0.1):
    """Sends key presses, supporting 6 keys at once as well as modifiers (to use multiple modifiers separate them via pipe (|))"""
    report = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for i, key in enumerate(keys):
        if isinstance(key, int):
            report[2 + i] = key
    
    with open(HID_DEVICE, "rb+") as fd:
        fd.write(bytes(report))
        time.sleep(delay)
        fd.write(bytes(8))

def hold_key(*keys):
    """Holds keys until the release function is called"""
    report = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for i, key in enumerate(keys):
        if isinstance(key, int):
            report[2 + i] = key
    
    with open(HID_DEVICE, "rb+") as fd:
        fd.write(bytes(report))

def release_keys():
    """Releases all currently held keys"""
    with open(HID_DEVICE, "rb+") as fd:
        fd.write(bytes(8))

def send_text(text, delay=0.1):
    """Sends a string of text, handling lowercase, uppercase, numbers, and special characters"""
    for char in text:
        if char.islower():
            send_key(char_to_keycode(char), delay=delay)
        elif char.isupper():
            send_key(KEY_LEFT_SHIFT, char_to_keycode(char), delay=delay)
        else:
            send_key(char_to_keycode(char), delay=delay)

# SiNGLE KEY REPORT FUNCTiONS
def send_enter(delay=0.1):
    """Sends the Enter key"""
    send_key(KEY_ENTER, delay=delay)

def send_space(delay=0.1):
    """Sends the Space key"""
    send_key(KEY_SPACE, delay=delay)

def send_tab(delay=0.1):
    """Sends the Tab key"""
    send_key(KEY_TAB, delay=delay)

def send_escape(delay=0.1):
    """Sends the Escape key"""
    send_key(KEY_ESC, delay=delay)
