import time

HID_DEVICE = "/dev/hidg0"

def send_key(modifier, key):
    report = bytes([modifier, 0, key, 0, 0, 0, 0, 0])
    with open(HID_DEVICE, "rb+") as fd:
        fd.write(report)  # press
        time.sleep(0.1)
        fd.write(bytes(8))  # release

KEY_A = 0x04
KEY_ENTER = 0x28
MOD_LEFT_CTRL = 0x01
MOD_LEFT_ALT = 0x04

send_key(0, KEY_A) # a
send_key(MOD_LEFT_CTRL, KEY_A) # ctrl a
send_key(MOD_LEFT_CTRL | MOD_LEFT_ALT, KEY_A) # ctrl alt a
send_key(0, KEY_ENTER) # enter
