# HIDPi
## About This Project
This project focuses on a simple way to set up a Raspberry Pi 4B (and maybe others) as a USB HID device. 

I created this because I was getting really annoyed about the lack of info on using Pis other than the Zero as USB HID devices. There are many posts that mention doing it, but they never seem to work. There are also many posts saying only the Pico or Zero can do it.

I've tested it on a Raspberry Pi 4B 8GB model from 2018, running Raspberry Pi OS lite (32-bit), Debian Bookworm. It probably works on 64-bit but I haven't tried it yet.

## Install

### 2 Commands
Simply run this (you may have to run `sudo apt upgrade -y` after `sudo apt update`)
```sh
sudo apt update && sudo apt install libusb-1.0-0-dev libudev-dev -y && curl https://raw.githubusercontent.com/rikka-chunibyo/HIDPi/refs/heads/master/HIDPi_Setup.py -o HIDPi_Setup.py && sudo python3 HIDPi_Setup.py
```
It will reboot itself, and that's all! Take a look at [Usage](#usage) for an example on how to use HIDPi

### Casual
Or if you want to go through it yourself (you may have to run `sudo apt upgrade -y` after `sudo apt update`)
```sh
sudo apt update
sudo apt install libusb-1.0-0-dev libudev-dev -y
curl https://raw.githubusercontent.com/rikka-chunibyo/HIDPi/refs/heads/master/HIDPi_Setup.py -o HIDPi_Setup.py
sudo python3 HIDPi_Setup.py
```
It will reboot itself, and that's all! Take a look at [Usage](#usage) for an example on how to use HIDPi

### Manual
If you're looking to run each individual command in the Python installer, follow this guide [HIDPi_Setup.md](https://github.com/rikka-chunibyo/HIDPi/blob/fd94a5a43bf75b7723eb34bdf506ec681762cc8b/HIDPi_Setup.md).

### Troubleshooting and Customizing the Install
Check if `/dev/hidg0` exists, if it doesn't make sure to check under different numbers. If it still doesn't exist, try running the setup again (don't reinstall the OS or anything, just run the setup again). If this works most likely the service failed to start for some reason, create an issue with the logs (get them with 
```sh
journalctl -xeu HIDPi
```

If the install fails for whatever reason you can try installing it by following the AI-generated guide [HIDPi_Setup.md](https://github.com/rikka-chunibyo/HIDPi/blob/fd94a5a43bf75b7723eb34bdf506ec681762cc8b/HIDPi_Setup.md), I have no clue if it's right, I didn't bother making it myself because the script hasn't failed for me. If the guide doesn't work feel free to create an issue and I'll rewrite it myself.

If you want to edit the reported device details, just edit these using nano before running the script. If using the tutorial you can easily change them before copying the commands.
https://github.com/rikka-chunibyo/HIDPi/blob/47cc064092268af990a6a4d0df06f5e000bdeb40/HIDPi_Setup.py#L37-L39

## Usage
Since it's so basic of an implementation (seriously why can't I find another repo on this that just works???), the code is slightly more in-depth then your common HID libraries, but it's still really simple. I'll probably make a library for it soon which literally just removes the need to manually add the keys.

Here's an example
https://github.com/rikka-chunibyo/HIDPi/blob/04c8afad249296d99caa07483bd45afe567e3fc7/Example_Usage.py#L1-L19

Sendkey format is very simple

![](assets/sendkey.png)

Just have to convert it using [this](https://usb.org/sites/default/files/documents/hut1_12v2.pdf#10%20Keyboard/Keypad%20Page%20(0x07)) table

## Issues
I usually respond fast, I honestly don't know much about all of this, I just scrapped together some commands and stuff, but I'll try my best to help. 

If there's an issue while your using a different OS, please open an issue about adding support for it, I'd like this project to be as plug-and-play and simple as possible.

Not really about issues but if you have any suggestions for improvements or anything feel free to open a discussion about it.
