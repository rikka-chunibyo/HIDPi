import time
from .keyboard_keys import *

HID_DEVICE = "/dev/hidg0"

class Keyboard:
    @staticmethod
    def char_to_keycode(char):
        char_lowered = char.lower()
        return KEY_MAPPINGS.get(char_lowered, 0x00)

    @staticmethod
    def send_key(*keys, delay=0):
        report = [0] * 8
        for i, key in enumerate(keys[:6]):
            report[2 + i] = key
        Keyboard._send_report(bytes(report), delay)

    @staticmethod
    def hold_key(*keys):
        report = [0] * 8
        for i, key in enumerate(keys[:6]):
            report[2 + i] = key
        Keyboard._send_report(bytes(report), 0, False)

    @staticmethod
    def release_keys():
        Keyboard._send_report(bytes(8), 0, False)

    @staticmethod
    def send_text(text, delay=0):
        for char in text:
            if char.isupper():
                Keyboard.send_key(KEY_LEFT_SHIFT, Keyboard.char_to_keycode(char), delay=delay)
            else:
                Keyboard.send_key(Keyboard.char_to_keycode(char), delay=delay)

    @staticmethod
    def _send_report(report, delay=0, release=True):
        with open(HID_DEVICE, "rb+") as fd:
            fd.write(report)
            if delay: time.sleep(delay)
            if release: fd.write(bytes(8))
