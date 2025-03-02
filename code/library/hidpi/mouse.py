import time
from .mouse_buttons import *

MOUSE_DEVICE = "/dev/hidg1"

class Mouse:
    @staticmethod
    def move(x, y, wheel=0, delay=0):
        report = bytes([0, x & 0xFF, y & 0xFF, wheel & 0xFF])
        Mouse._send_report(report, delay)

    @staticmethod
    def click(button, delay=0):
        Mouse._send_report(bytes([button, 0, 0, 0]), delay)
        Mouse._send_report(bytes([0, 0, 0, 0]), delay)

    @staticmethod
    def _send_report(report, delay=0):
        with open(MOUSE_DEVICE, "rb+") as fd:
            fd.write(report)
            if delay: time.sleep(delay)
            fd.write(bytes([0, 0, 0, 0]))
