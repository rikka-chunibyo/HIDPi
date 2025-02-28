import os
import time
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Error: {err.decode().strip()}")
    else:
        print(out.decode().strip())

# def run_logged_command(command):
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     for line in iter(process.stdout.readline, b''):
#         print(line.decode().strip())
#     for line in iter(process.stderr.readline, b''):
#         print(line.decode().strip())
#     process.stdout.close()
#     process.stderr.close()
#     process.wait()
#     if process.returncode != 0:
#         print(f"Error: Process ended with non-zero exit code {process.returncode}")

def modify_config_txt():
    config_file = "/boot/firmware/config.txt"
    lines_to_add = ["dtoverlay=dwc2", "modules-load=dwc2,g_hid"]
    
    with open(config_file, "a") as f:
        f.write("\n" + "\n".join(lines_to_add) + "\n")
    
    print("Added to /boot/firmware/config.txt.")
    time.sleep(2)

# def install_dependencies():
#     print("Installing dependencies... (this may take a while)")
#     time.sleep(2)
#     run_command("sudo apt update")
#     run_command("sudo apt install libusb-1.0-0-dev libudev-dev")

def setup_hid_gadget():
    print("Setting up HID gadget...")
    run_command("sudo modprobe libcomposite")
    run_command("cd /sys/kernel/config/usb_gadget/ && sudo mkdir -p hid_gadget")
    run_command("cd /sys/kernel/config/usb_gadget/hid_gadget && echo 0x1d6b > idVendor")
    run_command("cd /sys/kernel/config/usb_gadget/hid_gadget && echo 0x0104 > idProduct")
    
    # Setting device details
    run_command("mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409")
    run_command("echo '1234567890' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/serialnumber")
    run_command("echo 'Rikka' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/manufacturer")
    run_command("echo 'HIDPi' > /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/product")
    
    # HID function configuration
    run_command("mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0")
    run_command("echo 1 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/protocol")
    run_command("echo 1 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/subclass")
    run_command("echo 8 > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/report_length")
    
    # Create a temporary file to hold the report descriptor
    report_desc = b"\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x01\x95\x06\x75\x08\x15\x00\x26\xa4\x00\x05\x07\x19\x00\x29\xa4\x81\x00\xc0"
    
    # Write the report descriptor to a temporary file
    with open("/tmp/report_desc.bin", "wb") as f:
        f.write(report_desc)
    
    # Copy the report descriptor to file
    run_command("sudo cat /tmp/report_desc.bin > /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/report_desc")
    
    # Link the HID function
    run_command("mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409")
    run_command("echo 'Config 1' > /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409/configuration")
    run_command("echo 250 > /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/MaxPower")
    run_command("ln -s /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0 /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/")
    
    # Enable the gadget
    run_command("ls /sys/class/udc > /sys/kernel/config/usb_gadget/hid_gadget/UDC")

def create_udev_rule():
    print("Creating udev rule for hidg...")
    udev_rule = "/etc/udev/rules.d/99-hidg.rules"
    with open(udev_rule, "a") as f:
        f.write("KERNEL==\"hidg*\", MODE=\"0666\"\n")
    
    run_command("sudo udevadm control --reload-rules")
    print("Udev rules reloaded. Please reboot your system.")

def main():
    modify_config_txt()
    # install_dependencies()
    setup_hid_gadget()
    create_udev_rule()
    print("Script execution complete. Please reboot your system. After reboot `/dev/hidg0` should be available. If it isn't available, check under different numbers. If it still isn't available, you may have to run the setup file again (don't reinstall OS, literally just rerun the setup after reboot)")

if __name__ == "__main__":
    main()
