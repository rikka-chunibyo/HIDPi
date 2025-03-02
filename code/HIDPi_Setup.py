import os
import shutil
import time
import subprocess

INSTALL_PATH = "/usr/local/bin/HIDPi.py"
SERVICE_NAME = "HIDPi"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}.service"
CONFIG_FILE = "/boot/firmware/config.txt"
LINES_TO_ADD = ["dtoverlay=dwc2", "modules-load=dwc2,g_hid"]

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
        "mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409",
        "echo '1234567890' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/serialnumber",
        "echo 'Rikka' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/manufacturer",
        "echo 'HIDPi' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/product"
    ]

    for cmd in commands:
        run_command(cmd)

    # KEYBOARD
    run_command("mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0")
    run_command("echo 1 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/protocol")
    run_command("echo 1 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/subclass")
    run_command("echo 8 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/report_length")

    keyboard_desc = b"\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x01\x95\x06\x75\x08\x15\x00\x26\xa4\x00\x05\x07\x19\x00\x29\xa4\x81\x00\xc0"
    with open("/sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/report_desc", "wb") as f:
        f.write(keyboard_desc)

    # MOUSE
    run_command("mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb1")
    run_command("echo 1 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb1/protocol")
    run_command("echo 1 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb1/subclass")
    run_command("echo 4 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb1/report_length")

    mouse_desc = b"\x05\x01\x09\x02\xa1\x01\x09\x01\xa1\x00\x05\x09\x19\x01\x29\x03\x15\x00\x25\x01\x75\x01\x95\x03\x81\x02\x75\x05\x95\x01\x81\x01\x05\x01\x09\x30\x09\x31\x15\x81\x25\x7f\x75\x08\x95\x02\x81\x06\xc0\xc0"
    with open("/sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb1/report_desc", "wb") as f:
        f.write(mouse_desc)

    # CONTROLLER
    # run_command("mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb2")
    # run_command("echo 1 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb2/protocol")
    # run_command("echo 1 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb2/subclass")
    # run_command("echo 64 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb2/report_length")

    # gamepad_desc = b"\x05\x01\x09\x05\xa1\x01\xa1\x02\x85\x01\x05\x09\x19\x01\x29\x10\x15\x00\x25\x01\x75\x01\x95\x10\x81\x02\x05\x01\x09\x30\x09\x31\x09\x32\x09\x35\x15\x81\x25\x7f\x75\x08\x95\x04\x81\x02\xc0\xc0"
    # with open("/sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb2/report_desc", "wb") as f:
    #     f.write(gamepad_desc)


    # CONFiGURE GADGET
    run_command("mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409")
    run_command("echo 'Config 1' > /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409/configuration")
    run_command("echo 250 > /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/MaxPower")

    # LiNK FUNCTiONS TO GADGET CONFiG
    run_command("ln -s /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0 /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/")
    run_command("ln -s /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb1 /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/")
    # run_command("ln -s /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb2 /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/")

    run_command("ls /sys/class/udc > /sys/kernel/config/usb_gadget/hid_gadget/UDC")

def create_udev_rule():
    print("Creating udev rule for hidg...")
    udev_rule = "/etc/udev/rules.d/99-hidg.rules"
    with open(udev_rule, "w") as f:
        f.write('KERNEL=="hidg*", MODE="0666"\n')
    
    run_command("sudo udevadm control --reload-rules")
    run_command("sudo chmod 666 /dev/hidg*")
    print("Udev rules reloaded.")

def main():
    install_self()
    modify_config_txt()
    setup_hid_gadget()
    create_udev_rule()
    print("HIDPi Initialized")

if __name__ == "__main__":
    main()
