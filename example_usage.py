import time

HID_DEVICE = "/dev/hidg0"

def send_key(modifier, key):
    report = bytes([modifier, 0, key, 0, 0, 0, 0, 0])
    with open(HID_DEVICE, "rb+") as fd:
        fd.write(report)  # press
        time.sleep(0.1)
        fd.write(bytes(8))  # release

# https://usb.org/sites/default/files/documents/hut1_12v2.pdf page 53
KEY_A = 0x04
KEY_ENTER = 0x28
MOD_LEFT_CTRL = 0x01

send_key(0, KEY_A) # a
send_key(MOD_CTRL, KEY_A) # ctrl a
send_key(0, KEY_ENTER) # enter
