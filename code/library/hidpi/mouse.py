import time

MOUSE_DEVICE = "/dev/hidg1"

class Mouse:
    @staticmethod
    def move(x, y, wheel=0):
        report = bytes([0, x & 0xFF, y & 0xFF, wheel & 0xFF])
        with open(MOUSE_DEVICE, "rb+") as fd:
            fd.write(report)

    @staticmethod
    def click(button=1):
        """(1: left, 2: right, 4: middle)"""
        Mouse._send_report(button)
        Mouse._send_report(0)

    @staticmethod
    def _send_report(button):
        report = bytes([button, 0, 0, 0])
        with open(MOUSE_DEVICE, "rb+") as fd:
            fd.write(report)