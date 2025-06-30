import os
import shutil
import subprocess
import time
import sys

if os.geteuid() != 0:
    print("This script must be run as root.")
    sys.exit(1)

SERIAL_NUMBER = "1234567890"
MANUFACTURER = "Rikka"
PRODUCT = "HIDPi"

INSTALL_PATH = "/usr/local/bin/HIDPi.py"
PYTHON_LOCATION = "/usr/bin/python3"
SERVICE_NAME = "HIDPi"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}.service"

# manually change if this doesn't work for you for whatever reason
FIRMWARE_CONFIG_FILE = (
    "/boot/firmware/config.txt" if os.path.exists("/boot/firmware/config.txt")
    else "/boot/config.txt"
)

LINES_TO_ADD = [
    "dtoverlay=dwc2",
    "modules-load=dwc2,g_hid"
]

# internal use only
paths = []

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Error: {err.decode().strip()}")
    else:
        print(out.decode().strip())

def run_commands(commands):
    for command in commands:
        run_command(command)


# --- INSTALL ---
def install_self():
    if os.path.abspath(__file__) != INSTALL_PATH:
        print("Copying script to " + INSTALL_PATH + "...")
        shutil.copy(__file__, INSTALL_PATH)
        os.chmod(INSTALL_PATH, 0o755)

    service_content = f"""[Unit]
Description=HIDPi Initialization
After=network.target multi-user.target
Wants=multi-user.target

[Service]
Type=oneshot
ExecStart={PYTHON_LOCATION} {INSTALL_PATH}
RemainAfterExit=yes
User=root

[Install]
WantedBy=multi-user.target
"""
    print("Creating systemd service...")
    with open(SERVICE_PATH, "w") as f:
        f.write(service_content)

    run_commands([
        "systemctl daemon-reload",
        f"systemctl enable {SERVICE_NAME}.service"
    ])
    print(f"{SERVICE_NAME} service installed. It will run on next boot")

def check_config():
    try:
        with open(FIRMWARE_CONFIG_FILE, 'r') as file:
            config_content = file.read()
            return all(line in config_content for line in LINES_TO_ADD)
    except FileNotFoundError:
        print(f"Firmware config file {FIRMWARE_CONFIG_FILE} not found!")
        return False

def modify_config_txt():
    if check_config():
        print("Config already modified")
    else:
        print("Modifying " + FIRMWARE_CONFIG_FILE + "...")
        with open(FIRMWARE_CONFIG_FILE, "a") as f:
            f.write("\n" + "\n".join(LINES_TO_ADD) + "\n")

        print("Config updated. Please reboot to apply changes. Once booted, the HIDPi service will finish the setup")
        sys.exit(0)

def wait_for_udc(timeout=10):
    udc_path = "/sys/class/udc"
    elapsed = 0
    while elapsed < timeout:
        try:
            devices = os.listdir(udc_path)
            if devices:
                print(f"Found UDC device: {devices[0]}")
                return devices[0]
        except Exception:
            pass
        time.sleep(1)
        elapsed += 1
    print("Timeout waiting for UDC device")
    return None

def create_device(path, protocol, subclass, report_length, report_desc_bytes):
    fullPath = os.path.join("/sys/kernel/config/usb_gadget/hid_gadget/functions", path)
    os.makedirs(fullPath, exist_ok=True)

    for name, value in [("protocol", protocol), ("subclass", subclass), ("report_length", report_length)]:
        with open(f"{fullPath}/{name}", "w") as f:
            f.write(str(value))

    with open(f"{fullPath}/report_desc", "wb") as f:
        f.write(report_desc_bytes)

    paths.append(fullPath)

def setup_hid_gadget():
    print("Setting up HID gadget...")
    run_commands([
        "modprobe dwc2",
        "modprobe libcomposite"
    ])

    # CREATE HID GADGET
    run_commands([
        "mkdir -p /sys/kernel/config/usb_gadget/hid_gadget",
        "mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409",
        "mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409"
    ])

    for name, value in [
        ("idVendor", "0x1d6b"),
        ("idProduct", "0x0104"),
        ("strings/0x409/serialnumber", SERIAL_NUMBER),
        ("strings/0x409/manufacturer", MANUFACTURER),
        ("strings/0x409/product", PRODUCT),
        ("configs/c.1/strings/0x409/configuration", "Default"),
        ("configs/c.1/MaxPower", "250")
    ]:
        with open(f"/sys/kernel/config/usb_gadget/hid_gadget/{name}", "w") as f:
            f.write(str(value))

    # KEYBOARD
    create_device("hid.usb0", 1, 1, 8, (
        b"\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01"
        b"\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x05\x75\x01"
        b"\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x01\x95\x06"
        b"\x75\x08\x15\x00\x26\xa4\x00\x05\x07\x19\x00\x29\xa4\x81\x00\xc0"
    ))

    # MOUSE
    create_device("hid.usb1", 1, 1, 4, (
        b"\x05\x01\x09\x02\xa1\x01\x09\x01\xa1\x00\x05\x09\x19\x01\x29\x03"
        b"\x15\x00\x25\x01\x75\x01\x95\x03\x81\x02\x75\x05\x95\x01\x81\x01"
        b"\x05\x01\x09\x30\x09\x31\x15\x81\x25\x7f\x75\x08\x95\x02\x81\x06"
        b"\xc0\xc0"
    ))

    # LiNK FUNCTiONS TO GADGET CONFiG
    for p in paths:
        link_path = f"/sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/{os.path.basename(p)}"
        if not os.path.exists(link_path):
            os.symlink(p, link_path)

    udc_device = wait_for_udc(timeout=15)
    if udc_device:
        with open("/sys/kernel/config/usb_gadget/hid_gadget/UDC", "w") as f:
            f.write(udc_device)
        print(f"Bound gadget to UDC: {udc_device}")
    else:
        print("Failed to bind gadget to UDC device")

def create_udev_rule():
    print("Creating udev rule for hidg...")
    udev_rule = "/etc/udev/rules.d/99-hidg.rules"
    with open(udev_rule, "w") as f:
        f.write('KERNEL=="hidg*", SUBSYSTEM=="hidg", MODE="0666", TAG+="uaccess"\n')

    run_command("udevadm control --reload-rules")
    run_command("chmod 666 /dev/hidg*")
    print("Udev rules reloaded")


# --- UNINSTALL ---
def remove_service():
    if os.path.exists(SERVICE_PATH):
        print("Removing systemd service...")
        run_commands([
            f"systemctl disable {SERVICE_NAME}.service",
            f"rm -f {SERVICE_PATH}"
        ])
        print("Service removed")

def remove_installed_script():
    if os.path.exists(INSTALL_PATH):
        os.remove(INSTALL_PATH)
        print("Removed installed script")

def remove_gadget():
    print("Removing HID gadget...")
    udc_path = "/sys/kernel/config/usb_gadget/hid_gadget/UDC"
    if os.path.exists(udc_path):
        try:
            with open(udc_path, "w") as f:
                f.write("")
            print("Unbound gadget from UDC")
        except Exception as e:
            print(f"Failed to unbind UDC: {e}")
    run_command("rm -rf /sys/kernel/config/usb_gadget/hid_gadget")

def remove_udev_rule():
    rule_path = "/etc/udev/rules.d/99-hidg.rules"
    if os.path.exists(rule_path):
        os.remove(rule_path)
        print("Udev rule removed")
    run_command("udevadm control --reload-rules")



# --- MAIN ---
def install():
    install_self()
    modify_config_txt()
    setup_hid_gadget()
    create_udev_rule()
    print("HIDPi Initialized")

def uninstall():
    print("Uninstalling HIDPi...")
    remove_gadget()
    remove_udev_rule()
    remove_service()
    remove_installed_script()
    print(f"Uninstallation complete. You may need to modify {FIRMWARE_CONFIG_FILE} manually, as I'd rather not risk breaking your system")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        install() # also runs on boot
    elif args[0] in ("uninstall", "remove"):
        uninstall()
    elif args[0] in ("--help", "-h"):
        print("""Usage:
    sudo python3 HIDPi.py                       # install and activate
    sudo python3 HIDPi.py uninstall             # revert all* changes
      """)
    else:
        print(f"Unknown argument: {args[0]}")
        print("Run with --help or -h for usage")
