"""
HIDPi Module
============

This module provides an interface for controlling a HID keyboard and mouse on a Raspberry Pi.

Modules:
--------
- `Keyboard`: Provides methods to send keystrokes.
- `Mouse`: Provides methods to control mouse movement and clicks.

Version:
--------
- `1.1`
"""

__version__ = '1.1'

from .keyboard import Keyboard
from .mouse import Mouse
