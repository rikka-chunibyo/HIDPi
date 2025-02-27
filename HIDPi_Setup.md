I had ChatGPT make an install tutorial for if the script ever fails, enjoy!

Here’s a step-by-step tutorial for setting up the HID gadget on a 
Raspberry Pi using shell commands. If the provided script doesn’t work, 
you can manually follow these steps to configure your Raspberry Pi. The 
setup will make the Pi act as an HID device, which can emulate keyboards 
or mice.

## Setup HID Gadget on Raspberry Pi

### Prerequisites:
Ensure your Raspberry Pi has access to the internet for installing 
dependencies and modifying system files.

---

### 1. Modify `/boot/firmware/config.txt`

This step ensures that the necessary overlays and modules are enabled for 
HID functionality.

```bash
sudo nano /boot/firmware/config.txt
```

Add the following lines at the end of the file:

```
dtoverlay=dwc2
modules-load=dwc2,g_hid
```

Save the file by pressing `Ctrl+X`, then `Y`, and finally `Enter`.

---

### 2. Install Dependencies

You need to install several dependencies to enable HID gadget 
functionality.

```bash
sudo apt update
sudo apt install libusb-1.0-0-dev libudev-dev python3-pip
```

---

### 3. Setup HID Gadget

Now, let's set up the HID gadget manually by executing the following 
commands. These commands will configure the USB gadget driver, set the 
necessary device parameters, and prepare the gadget to be recognized by 
the system.

```bash
# Load the necessary kernel module
sudo modprobe libcomposite

# Create the USB gadget directory structure
cd /sys/kernel/config/usb_gadget/ && sudo mkdir -p hid_gadget

# Set vendor and product IDs
cd /sys/kernel/config/usb_gadget/hid_gadget && echo 0x1d6b > idVendor
cd /sys/kernel/config/usb_gadget/hid_gadget && echo 0x0104 > idProduct

# Set device strings (optional, but recommended)
mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/strings/0x409
echo '1234567890' > 
/sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/serialnumber
echo 'Raspberry Pi' > 
/sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/manufacturer
echo 'Pi HID Device' > 
/sys/kernel/config/usb_gadget/hid_gadget/strings/0x409/product

# Set up the HID function
mkdir -p /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0
echo 1 > 
/sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/protocol
echo 1 > 
/sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/subclass
echo 8 > 
/sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/report_length
```

Create the report descriptor file, which specifies the functionality of 
the HID device:

```bash
# Create a temporary report descriptor file
echo -n -e 
"\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x01\x95\x06\x75\x08\x15\x00\x26\xa4\x00\x05\x07\x19\x00\x29\xa4\x81\x00\xc0" 
> /tmp/report_desc.bin

# Copy the report descriptor to the gadget configuration
sudo cat /tmp/report_desc.bin > 
/sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0/report_desc
```

Link the HID function to the gadget’s configuration:

```bash
mkdir -p 
/sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409
echo 'Config 1' > 
/sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/strings/0x409/configuration
echo 250 > /sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/MaxPower

# Link the HID function to the configuration
ln -s /sys/kernel/config/usb_gadget/hid_gadget/functions/hid.usb0 
/sys/kernel/config/usb_gadget/hid_gadget/configs/c.1/
```

Finally, enable the gadget:

```bash
# Enable the USB gadget
ls /sys/class/udc > /sys/kernel/config/usb_gadget/hid_gadget/UDC
```

---

### 4. Create a Udev Rule

Create a `udev` rule to allow the `hidg` device to be accessed by any 
user:

```bash
sudo nano /etc/udev/rules.d/99-hidg.rules
```

Add the following line:

```
KERNEL=="hidg*", MODE="0666"
```

Save the file by pressing `Ctrl+X`, then `Y`, and finally `Enter`.

---

### 5. Reload Udev Rules

Reload the `udev` rules to apply the changes:

```bash
sudo udevadm control --reload-rules
```

---

### 6. Reboot Your Raspberry Pi

After completing the steps, reboot your Raspberry Pi:

```bash
sudo reboot
```

After rebooting, the HID gadget should be available as `/dev/hidg0`. If it 
is not available, try checking under different numbers (`/dev/hidg1`, 
etc.). If the device still doesn’t show up, rerun the setup process.

---

### Troubleshooting:

- If the device does not show up, verify that all modules are loaded 
correctly and that the kernel supports HID gadgets.
- Ensure that the gadget is linked properly by checking the directory 
structure in `/sys/kernel/config/usb_gadget/`.


