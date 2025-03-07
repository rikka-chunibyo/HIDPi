import os
import shutil
import time
import subprocess

INSTALL_PATH = "/usr/local/bin/HIDPi.py"
SERVICE_NAME = "HIDPi"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}.service"
CONFIG_FILE = "/boot/firmware/config.txt"
LINES_TO_ADD = ["dtoverlay=dwc2", "modules-load=dwc2,g_hid"]

HID_DESCRIPTOR = {
    # Keyboard
    0x05, 0x01,                     # Usage Page (Generic Desktop Ctrls)
    0x09, 0x06,                     # Usage (Keyboard)
    0xA1, 0x01,                     # Collection (Application)
    0x85, 0x01,                     #   Report ID (1)
    0x05, 0x07,                     #   Usage Page (Kbrd/Keypad)
    0x75, 0x01,                     #   Report Size (1)
    0x95, 0x08,                     #   Report Count (8)
    0x19, 0xE0,                     #   Usage Minimum (0xE0)
    0x29, 0xE7,                     #   Usage Maximum (0xE7)
    0x15, 0x00,                     #   Logical Minimum (0)
    0x25, 0x01,                     #   Logical Maximum (1)
    0x81, 0x02,                     #   Input (Data,Var,Absolute)
    0x95, 0x01,                     #   Report Count (1)
    0x75, 0x08,                     #   Report Size (8)
    0x15, 0x00,                     #   Logical Minimum (0)
    0x25, 0x64,                     #   Logical Maximum (100)
    0x05, 0x07,                     #   Usage Page (Kbrd/Keypad)
    0x19, 0x00,                     #   Usage Minimum (0x00)
    0x29, 0x65,                     #   Usage Maximum (0x65)
    0x81, 0x00,                     #   Input (Data,Array,Absolute)
    0xC0,                           # End Collection

    # Mouse
    0x05, 0x01,                     # USAGE_PAGE (Generic Desktop)
    0x09, 0x02,                     # USAGE (Mouse)
    0xa1, 0x01,                     # COLLECTION (Application)
    0x85, 0x02,                     #   Report ID (2)
    0x09, 0x01,                     #   USAGE (Pointer)
    0xA1, 0x00,                     #   COLLECTION (Physical)
    0x05, 0x09,                     #     USAGE_PAGE (Button)
    0x19, 0x01,                     #     USAGE_MINIMUM
    0x29, 0x03,                     #     USAGE_MAXIMUM
    0x15, 0x00,                     #     LOGICAL_MINIMUM (0)
    0x25, 0x01,                     #     LOGICAL_MAXIMUM (1)
    0x95, 0x03,                     #     REPORT_COUNT (3)
    0x75, 0x01,                     #     REPORT_SIZE (1)
    0x81, 0x02,                     #     INPUT (Data,Var,Abs)
    0x95, 0x01,                     #     REPORT_COUNT (1)
    0x75, 0x05,                     #     REPORT_SIZE (5)
    0x81, 0x03,                     #     INPUT (Const,Var,Abs)
    0x05, 0x01,                     #     USAGE_PAGE (Generic Desktop)
    0x09, 0x30,                     #     USAGE (X)
    0x09, 0x31,                     #     USAGE (Y)
    0x09, 0x38,                     #     USAGE (Wheel)
    0x15, 0x81,                     #     LOGICAL_MINIMUM (-127)
    0x25, 0x7F,                     #     LOGICAL_MAXIMUM (127)
    0x75, 0x08,                     #     REPORT_SIZE (8)
    0x95, 0x03,                     #     REPORT_COUNT (3)
    0x81, 0x06,                     #     INPUT (Data,Var,Rel)
    0xC0,                           #   END_COLLECTION
    0xC0,                           # END COLLECTION

    # Consumer Control
    0x05, 0x0c,                     # Usage Page (Consumer Devices)
    0x09, 0x01,                     # Usage (Consumer Control)
    0xa1, 0x01,                     # Collection (Application)
    0x85, 0x03,                     #   Report ID (3)
    0x19, 0x00,                     #   Usage Minimum (0),
    0x2A, 0xCD, 0x02,               #   Usage Maximum (0x23C),
    0x15, 0x00,                     #   Logical Minimum (0)
    0x26, 0x3C, 0x02,               #   Logical Maximum (0x23C)
    0x75, 0x10,                     #   Report Size (10)
    0x95, 0x01,                     #   Report Count (1)
    0x81, 0x00,                     #   Input (Data,Array,Absolute)
    0xC0,                           # End Collection

    # Touch Screen
    0x05, 0x0D,                 # Usage Page (Digitizers)
    0x09, 0x04,                 # Usage (Touch Screen)
    0xA1, 0x01,                 # Collection (Application)
    0x85, 0x04,                 #   Report ID (4)
    0x09, 0x22,                 #   Usage (Finger)
    0xA1, 0x02,                 #   Collection (Logical)
    0x09, 0x42,                 #     Usage (Tip Switch)
    0x09, 0x32,                 #     Usage (In Range)
    0x15, 0x00,                 #     Logical Minimum (0)
    0x25, 0x01,                 #     Logical Maximum (1)
    0x75, 0x01,                 #     Report Size (1)
    0x95, 0x02,                 #     Report Count (2) -> (Tip Switch and In Range)
    0x81, 0x02,                 #     Input (Data, Variable, Absolute)
    0x95, 0x06,                 #     Report Count (6) -> padding bits
    0x81, 0x03,                 #     Input (Constant, Variable, Absolute)
    0x05, 0x01,                 #     Usage Page (Generic Desktop)
    0x09, 0x30,                 #     Usage (X)
    0x09, 0x31,                 #     Usage (Y)
    0x16, 0x00, 0x00,           #     Logical Minimum (0)
    0x26, 0xFF, 0x7F,           #     Logical Maximum (32767)
    0x36, 0x00, 0x00,           #     Physical Minimum (0)
    0x46, 0xFF, 0x7F,           #     Physical Maximum (32767)
    0x75, 0x10,                 #     Report Size (16)
    0x95, 0x02,                 #     Report Count (2) -> (X, Y coordinates)
    0x81, 0x02,                 #     Input (Data, Variable, Absolute)
    0xC0,                       #   End Collection (Logical)
    0xC0,                       # End Collection (Application)
}

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Error: {err.decode().strip()}")
    else:
        print(out.decode().strip())

def install_self():
    if os.path.abspath(__file__) != INSTALL_PATH:
        print("Copying script to /usr/local/bin/...")
        shutil.copy(__file__, INSTALL_PATH)
        os.chmod(INSTALL_PATH, 0o755)

    service_content = f"""[Unit]
Description=HIDPi Initialization
After=network.target

[Service]
ExecStart=/usr/bin/python3 {INSTALL_PATH}
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
"""
    print("Creating systemd service...")
    with open(SERVICE_PATH, "w") as f:
        f.write(service_content)

    run_command("sudo systemctl daemon-reload")
    run_command(f"sudo systemctl enable {SERVICE_NAME}.service")
    print(f"{SERVICE_NAME} service installed. It will run on next boot.")
    
def check_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            config_content = file.read()
            return all(line in config_content for line in LINES_TO_ADD)
    except FileNotFoundError:
        print(f"Boot config file {CONFIG_FILE} not found!")
        return False

def modify_config_txt():
    if check_config():
        print("Config already modified.")
    else:
        print("Modifying /boot/firmware/config.txt...")
        with open(CONFIG_FILE, "a") as f:
            f.write("\n" + "\n".join(LINES_TO_ADD) + "\n")

        print("Config updated. Rebooting in 10 seconds... Once booted, you should be able to access `/dev/hidg0`")
        time.sleep(10)
        run_command("sudo reboot")

def setup_hid_gadget():
    print("Setting up HID gadget...")
    commands = [
        "sudo modprobe libcomposite",
        "mkdir -p /sys/kernel/config/usb_gadget/hid_gadget",

        "echo 0x1d6b > /sys/kernel/config/usb_gadget/hid_gadget/idVendor",
        "echo 0x0104 > /sys/kernel/config/usb_gadget/hid_gadget/idProduct",
        "echo 0x0409 > /sys/kernel/config/usb_gadget/hid_gadget/bcdDevice",
        "echo 0x0200 > /sys/kernel/config/usb_gadget/hid_gadget/bcdUSB",

        "mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409",
        "echo 'Rikka' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/manufacturer",
        "echo 'HIDPi' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/product",
        "echo '123456789' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/serialnumber",

        "mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409",
        "echo 'Config 1' > /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409/configuration",

        # Other Configuration
        "echo 900 > /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/MaxPower",  # Power (Milliamps)

        "mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0",
        f"echo {','.join(map(str, hid_descriptor))} > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/report_desc",
        "ln -s /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0 /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1",
        "echo '1' > /sys/kernel/config/usb_gadget/hid_gadget/UDC"
    ]

    for cmd in commands:
        run_command(cmd)

def main():
    install_self()
    modify_config_txt()
    setup_hid_gadget()

if __name__ == "__main__":
    main()
