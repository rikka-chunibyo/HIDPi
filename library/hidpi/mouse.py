"""
The Mouse class provides methods to control a HID mouse device.
It allows moving the cursor and simulating mouse clicks.
"""

import time
from .mouse_buttons import *

MOUSE_DEVICE = "/dev/hidg1"

class Mouse:
    """
    A class for controlling a HID-compliant mouse device.
    """

    @staticmethod
    def move(x, y, wheel=0):
        """
        Moves the mouse cursor by the specified x and y offsets.
        
        :param x: The movement offset along the X-axis.
        :type x: int
        :param y: The movement offset along the Y-axis.
        :type y: int
        :param wheel: The scroll wheel movement.
        :type wheel: int, optional
        """
        report = bytes([0, x & 0xFF, y & 0xFF, wheel & 0xFF])
        Mouse._send_report(report)

    @staticmethod
    def click(button, hold=0):
        """
        Simulates a mouse button click.
        
        :param button: The button to click (e.g., left, right, middle button).
        :type button: int
        :param hold: Time in seconds to hold the button before releasing.
        :type hold: float, optional
        """
        Mouse._send_report(bytes([button, 0, 0, 0]), hold)
        Mouse._send_report(bytes([0, 0, 0, 0]), hold)

    @staticmethod
    def _send_report(report, hold=0):
        """
        Sends a raw HID report to the mouse device.
        
        :param report: The raw HID report data.
        :type report: bytes
        :param hold: Time in seconds to wait after sending the report.
        :type hold: float, optional
        """
        with open(MOUSE_DEVICE, "rb+") as fd:
            fd.write(report)
            if hold:
                time.sleep(hold)
            fd.write(bytes([0, 0, 0, 0]))