# HIDPi
## About This Project
This project focuses on a simple way to set up a Raspberry Pi 4B (and maybe others) as a USB HID device. 

I created this because I was getting really annoyed about the lack of info on using Pis other than the Zero as USB HID devices. There are many posts that mention doing it, but they never seem to work. There are also many posts saying only the Pico or Zero can do it.

I've tested it on a Raspberry Pi 4B 8GB model from 2018, running Raspberry Pi OS lite (32-bit), Debian Bookworm. It probably works on 64-bit but I haven't tried it yet.

## Install

### One-Liner
Simply run this (you may have to run `sudo apt upgrade -y` after `sudo apt update`)
```sh
sudo apt update && sudo apt install libusb-1.0-0-dev libudev-dev -y && curl https://raw.githubusercontent.com/rikka-chunibyo/HIDPi/refs/heads/master/code/HIDPi_Setup.py -o HIDPi_Setup.py && sudo python3 HIDPi_Setup.py
```
It will reboot itself, and that's all! Take a look at [Usage](#usage) for an example on how to use HIDPi

### Casual
Or if you want to go through it yourself (you may have to run `sudo apt upgrade -y` after `sudo apt update`)
```sh
sudo apt update
sudo apt install libusb-1.0-0-dev libudev-dev -y
curl https://raw.githubusercontent.com/rikka-chunibyo/HIDPi/refs/heads/master/code/HIDPi_Setup.py -o HIDPi_Setup.py
sudo python3 HIDPi_Setup.py
```
It will reboot itself, and that's all! Take a look at [Usage](#usage) for an example on how to use HIDPi

### Manual
If you're looking to run each individual command in the Python installer, follow this guide [HIDPi_Setup.md](markdowns/HIDPi_Setup.md).

### Troubleshooting and Customizing the Install
If the install fails for whatever reason you can try installing it by following the AI-generated guide [HIDPi_Setup.md](markdowns/HIDPi_Setup.md).

If you want to edit the reported device details, just edit these using nano before running the script. If using the tutorial you can easily change them before copying the commands.
https://github.com/rikka-chunibyo/HIDPi/blob/5d8923c2a563fd5d4f914b0e31c02b067eabf2c9/code/HIDPi_Setup.py#L75-L77

If `/dev/hidg0` doesn't exist, make sure to check under different numbers. If it still doesn't exist, more likely than not, something went wrong with the service, check the logs with this
```sh
journalctl -xeu HIDPi
```
It should look something like this
```
Feb 28 02:10:30 rikka python3[1914]: Creating systemd service...
Feb 28 02:10:30 rikka python3[1914]: HIDPi service installed. It will run on next boot.
Feb 28 02:10:30 rikka python3[1914]: Config already modified.
Feb 28 02:10:30 rikka python3[1914]: Setting up HID gadget...
Feb 28 02:10:30 rikka python3[1914]: Error: /bin/sh: 1: echo: echo: I/O error
Feb 28 02:10:30 rikka python3[1914]: Error: /bin/sh: 1: echo: echo: I/O error
Feb 28 02:10:30 rikka python3[1914]: Error: /bin/sh: 1: echo: echo: I/O error
Feb 28 02:10:30 rikka python3[1914]: Error: cat: write error: Device or resource busy
Feb 28 02:10:30 rikka python3[1914]: Error: ln: failed to create symbolic link '/sys/kernel/config/usb_gadget/hid_g>
Feb 28 02:10:30 rikka python3[1914]: Error: ls: write error: Device or resource busy
Feb 28 02:10:30 rikka python3[1914]: Creating udev rule for hidg...
Feb 28 02:10:30 rikka python3[1914]: Udev rules reloaded.
Feb 28 02:10:30 rikka python3[1914]: HIDPi Initialized
Feb 28 02:10:30 rikka systemd[1]: HIDPi.service: Deactivated successfully.
░░ Subject: Unit succeeded
░░ Defined-By: systemd
░░ Support: https://www.debian.org/support
░░
░░ The unit HIDPi.service has successfully entered the 'dead' state.
```
It's okay to have those errors, if anything more than that fails, and you don't know how to resolve it, create an issue with the logs. It's okay to have what is shown faling in my log to fail, I just didn't make it stop trying those on reboot, which could have some benifits like fixing itself if something corrupts or gets deleted ¯\\\_(ツ)\_/¯ All it's doing is rerunning the installer via a service on startup.

## Usage
Since it's so basic of an implementation (seriously why can't I find another repo on this that just works???), the code is slightly more in-depth than your common HID libraries, but it's still really simple. I'll probably make a library for it soon which literally just removes the need to manually add the keys.

Here's an example
https://github.com/rikka-chunibyo/HIDPi/blob/f6ff2572d12a1d9b6094a15d0bf1f803020c49db/code/Example_Usage.py#L1-L20

Sendkey format is very simple

![](assets/sendkey.png)

> [!TIP]
> You can find info about keycodes using [this](https://usb.org/sites/default/files/documents/hut1_12v2.pdf#10%20Keyboard/Keypad%20Page%20(0x07)) table ([backup](assets/hut1_12v2.pdf) page 53)

## Issues
I usually respond fast, I honestly don't know much about all of this, I just scrapped together some commands and stuff, but I'll try my best to help. 

If there's an issue while your using a different OS, please open an issue about adding support for it, I'd like this project to be as plug-and-play and simple as possible.

Not really about issues but if you have any suggestions for improvements or anything feel free to open a discussion about it.

> [!NOTE]
> Keymap - Please tell me if something is wrong
```
| Usage ID | Key           | Usage ID | Key          | Usage ID | Key           | Usage ID | Key         |
|----------|---------------|----------|--------------|----------|---------------|----------|-------------|
| 0x00     | None          | 0x0D     | Tab          | 0x1A     | Z             | 0x27     | 0           |
| 0x01     | ErrorRollOver | 0x0E     | ` ~          | 0x1B     | X             | 0x28     | Enter       |
| 0x02     | LeftShift     | 0x0F     | - _          | 0x1C     | C             | 0x29     | Escape      |
| 0x03     | ErrorUndefined| 0x10     | = +          | 0x1D     | V             | 0x2A     | Backspace   |
| 0x04     | A             | 0x11     | [ {          | 0x1E     | B             | 0x2B     | Tab         |
| 0x05     | B             | 0x12     | ] }          | 0x1F     | M             | 0x2C     | Space       |
| 0x06     | C             | 0x13     | \ |          | 0x20     | N             | 0x2D     | - _         |
| 0x07     | D             | 0x14     | ; :          | 0x21     | , <           | 0x2E     | = +         |
| 0x08     | E             | 0x15     | ' "          | 0x22     | . >           | 0x2F     | [ {         |
| 0x09     | F             | 0x16     | ` ~          | 0x23     | / ?           | 0x30     | ] }         |
| 0x0A     | G             | 0x17     | CapsLock     | 0x24     | F1            | 0x31     | \ |         |
| 0x0B     | H             | 0x18     | LShift       | 0x25     | F2            | 0x32     | ; :         |
| 0x0C     | I             | 0x19     | LControl     | 0x26     | F3            | 0x33     | ' "         |
| 0x34     | ` ~           | 0x3A     | F9           | 0x40     | F15           | 0x4C     | Insert      |
| 0x35     | F1            | 0x3B     | F10          | 0x41     | F16           | 0x4D     | Home        |
| 0x36     | F2            | 0x3C     | F11          | 0x42     | F17           | 0x4E     | PageUp      |
| 0x37     | F3            | 0x3D     | F12          | 0x43     | F18           | 0x4F     | Delete      |
| 0x38     | F4            | 0x3E     | F13          | 0x44     | F19           | 0x50     | End         |
| 0x39     | F5            | 0x3F     | F14          | 0x45     | F20           | 0x51     | PageDown    |
| 0x52     | Up            | 0x53     | Down         | 0x54     | Right         | 0x55     | Left        |
| 0x56     | NumLock       | 0x57     | Keypad /     | 0x58     | Keypad *      | 0x59     | Keypad -    |
| 0x5A     | Keypad +      | 0x5B     | Keypad Enter | 0x5C     | Keypad 1      | 0x5D     | Keypad 2    |
| 0x5E     | Keypad 3      | 0x5F     | Keypad 4     | 0x60     | Keypad 5      | 0x61     | Keypad 6    |
| 0x62     | Keypad 7      | 0x63     | Keypad 8     | 0x64     | Keypad 9      | 0x65     | Keypad 0    |
| 0x66     | Keypad .      | 0x67     | Intl1        | 0x68     | Intl2         | 0x69     | Intl3       |
| 0x6A     | Intl4         | 0x6B     | Intl5        | 0x6C     | Intl6         | 0x6D     | Intl7       |
| 0x6E     | Intl8         | 0x6F     | Intl9        | 0x70     | Lang1         | 0x71     | Lang2       |
| 0x72     | Lang3         | 0x73     | Lang4        | 0x74     | Lang5         | 0x75     | Lang6       |
| 0x76     | Lang7         | 0x77     | Lang8        | 0x78     | Lang9         | 0x79     | AltErase    |
| 0x7A     | SysReq        | 0x7B     | Cancel       | 0x7C     | Clear         | 0x7D     | Prior       |
| 0x7E     | Return        | 0x7F     | Separator    | 0x80     | Out           | 0x81     | Oper        |
| 0x82     | ClearAgain    | 0x83     | CrSel        | 0x84     | ExSel         | 0xE0     | LeftCtrl    |
| 0xE1     | LeftAlt       | 0xE2     | RightShift   | 0xE3     | LeftControl   | 0xE4     | RightCtrl   |
| 0xE5     | RightShift    | 0xE6     | RightAlt     | 0xE7     | RightGUI      | 0xE8     | MediaPlay   |
| 0xE9     | MediaPause    | 0xEA     | MediaRecord  | 0xEB     | MediaFastForward| 0xEC   | MediaRewind |
| 0xED     | MediaNext     | 0xEE     | MediaPrevious| 0xEF     | MediaStop     | 0xF0     | MediaEject  |
```
