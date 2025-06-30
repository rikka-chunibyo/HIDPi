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
        return KEY_MAPPINGS.get(char.lower(), 0x00)

    @staticmethod
    def send_key(modifiers, *keys, hold=0):
        """
        Sends one or more key presses to the HID device, supporting modifier keys.

        :param modifiers: A byte representing the modifier keys (e.g., `KEY_LEFT_CTRL | KEY_LEFT_SHIFT` or `0` for no modifiers).
        :type modifiers: int
        :param keys: The keycodes to send (up to 6 keys can be sent at once).
        :type keys: int
        :param hold: Time in seconds to hold the keys before releasing them. Defaults to 0 (no hold).
        :type hold: float, optional
        """
        report = [0] * 8
        report[0] = modifiers

        for i, key in enumerate(keys[:6]):
            report[2 + i] = key

        Keyboard._send_report(bytes(report))
        if hold:
            time.sleep(hold)
        Keyboard.release_keys()

    @staticmethod
    def hold_key(modifiers, *keys):
        """
        Sends one or more key presses to the HID device without releasing them.

        :param modifiers: A byte representing the modifier keys (e.g., `KEY_LEFT_CTRL | KEY_LEFT_SHIFT` or `0` for no modifiers).
        :type modifiers: int
        :param keys: The keycodes to send (up to 6 keys can be sent at once).
        :type keys: int
        """
        report = [0] * 8
        report[0] = modifiers

        for i, key in enumerate(keys[:6]):
            report[2 + i] = key

        Keyboard._send_report(bytes(report))

    @staticmethod
    def release_keys():
        """
        Releases all currently held keys by sending an empty HID report.
        This simulates the release of any keys that may still be pressed.
        """
        Keyboard._send_report(bytes(8))

    @staticmethod
    def send_text(text, delay=0, hold=0):
        """
        Sends a string of text by converting characters to keycodes and simulating key presses.

        :param text: The text to send.
        :type text: str
        :param delay: Delay in seconds between each key press. Defaults to 0 (no delay).
        :type delay: float, optional
        :param hold: Time in seconds to hold the keys before releasing them. Defaults to 0 (no hold).
        :type hold: float, optional
        """
        for char in text:
            if delay:
                time.sleep(delay)
            keycode = Keyboard.char_to_keycode(char)
            if keycode:
                if char.isupper():
                    Keyboard.send_key(KEY_LEFT_SHIFT, keycode, hold=hold)
                else:
                    Keyboard.send_key(0, keycode, hold=hold)

    @staticmethod
    def _send_report(report):
        """
        Sends a raw HID report to the device.

        :param report: The raw HID report data to send to the HID device.
        :type report: bytes
        """
        with open(HID_DEVICE, "rb+") as fd:
            fd.write(report)
