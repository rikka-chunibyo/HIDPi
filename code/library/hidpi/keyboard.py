"""
The Keyboard class provides methods to send keystrokes to a HID device.
It supports modifier keys, key holding, text input, and key release.
"""

import time
from .keyboard_keys import *

HID_DEVICE = "/dev/hidg0"

class Keyboard:
    """
    A class for sending keystrokes to a HID keyboard device, with full support for modifier keys.
    """

    @staticmethod
    def char_to_keycode(char):
        """
        Converts a character to its corresponding HID keycode.

        :param char: The character to convert.
        :type char: str
        :return: The HID keycode for the given character, or 0x00 if not found.
        :rtype: int
        """
        char_lowered = char.lower()
        return KEY_MAPPINGS.get(char_lowered, 0x00)

    @staticmethod
    def send_key(modifiers, *keys, hold=0):
        """
        Sends one or more key presses to the HID device, supporting modifier keys.

        :param modifiers: A byte representing the modifier keys (e.g., `KEY_LEFT_CTRL | KEY_LEFT_SHIFT` or `0` for none).
        :type modifiers: int
        :param keys: The keycodes to send (up to 6).
        :type keys: int
        :param hold: Time in seconds to hold the keys before releasing.
        :type hold: float, optional
        """
        report = [0] * 8
        report[0] = modifiers

        for i, key in enumerate(keys[:6]):
            report[2 + i] = key

        Keyboard._send_report(bytes(report), delay=hold)

    @staticmethod
    def hold_key(modifiers, *keys):
        """
        Sends one or more key presses to the HID device without releasing them.

        :param modifiers: A byte representing the modifier keys (e.g., `KEY_LEFT_CTRL | KEY_LEFT_SHIFT` or `0` for none).
        :type modifiers: int
        :param keys: The keycodes to send (up to 6).
        :type keys: int
        """
        report = [0] * 8
        report[0] = modifiers

        for i, key in enumerate(keys[:6]):
            report[2 + i] = key

        Keyboard._send_report(bytes(report), release=False)

    @staticmethod
    def release_keys():
        """
        Releases all currently held keys by sending an empty HID report.
        """
        Keyboard._send_report(bytes(8), release=False)

    @staticmethod
    def send_text(text, delay=0):
        """
        Sends a string of text by converting characters to keycodes.

        :param text: The text to send.
        :type text: str
        :param delay: Delay in seconds between each key press.
        :type delay: float, optional
        """
        for char in text:
            keycode = Keyboard.char_to_keycode(char)
            if keycode:
                if char.isupper() or char in SHIFT_REQUIRED_KEYS:
                    Keyboard.send_key(KEY_LEFT_SHIFT, keycode, hold=delay)
                else:
                    Keyboard.send_key(0, keycode, hold=delay)

    @staticmethod
    def _send_report(report, delay=0, release=True):
        """
        Sends a raw HID report to the device.

        :param report: The raw HID report data.
        :type report: bytes
        :param delay: Time in seconds to wait after sending the report.
        :type delay: float, optional
        :param release: Whether to send an empty report to release the keys.
        :type release: bool, optional
        """
        with open(HID_DEVICE, "rb+") as fd:
            fd.write(report)
            if delay:
                time.sleep(delay)
            if release:
                fd.write(bytes(8))
