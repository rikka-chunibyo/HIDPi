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
| Usage ID | Key            | Usage ID | Key            | Usage ID | Key           | Usage ID | Key         |
|----------|----------------|----------|----------------|----------|---------------|----------|-------------|
| 0x00     | None           | 0x01     | ErrorRollOver  | 0x02     | POSTFail      | 0x03     | ErrorUndefined |
| 0x04     | A              | 0x05     | B              | 0x06     | C             | 0x07     | D           |
| 0x08     | E              | 0x09     | F              | 0x0A     | G             | 0x0B     | H           |
| 0x0C     | I              | 0x0D     | J              | 0x0E     | K             | 0x0F     | L           |
| 0x10     | M              | 0x11     | N              | 0x12     | O             | 0x13     | P           |
| 0x14     | Q              | 0x15     | R              | 0x16     | S             | 0x17     | T           |
| 0x18     | U              | 0x19     | V              | 0x1A     | W             | 0x1B     | X           |
| 0x1C     | Y              | 0x1D     | Z              | 0x1E     | 1             | 0x1F     | 2           |
| 0x20     | 3              | 0x21     | 4              | 0x22     | 5             | 0x23     | 6           |
| 0x24     | 7              | 0x25     | 8              | 0x26     | 9             | 0x27     | 0           |
| 0x28     | Enter          | 0x29     | Tab            | 0x2A     | Space         | 0x2B     | Backspace   |
| 0x2C     | LeftArrow      | 0x2D     | RightArrow     | 0x2E     | UpArrow       | 0x2F     | DownArrow   |
| 0x30     | PageUp         | 0x31     | PageDown       | 0x32     | Home          | 0x33     | End         |
| 0x34     | Insert         | 0x35     | Delete         | 0x36     | PrintScreen   | 0x37     | ScrollLock  |
| 0x38     | NumLock        | 0x39     | Keypad /       | 0x3A     | Keypad *      | 0x3B     | Keypad -    |
| 0x3C     | Keypad 7       | 0x3D     | Keypad 8       | 0x3E     | Keypad 9      | 0x3F     | Keypad +    |
| 0x40     | Keypad 4       | 0x41     | Keypad 5       | 0x42     | Keypad 6      | 0x43     | Keypad 1    |
| 0x44     | Keypad 2       | 0x45     | Keypad 3       | 0x46     | Keypad 0      | 0x47     | Keypad .    |
| 0x48     | LeftCtrl       | 0x49     | RightCtrl      | 0x4A     | LeftShift     | 0x4B     | RightShift  |
| 0x4C     | LeftAlt        | 0x4D     | RightAlt       | 0x4E     | LeftGUI       | 0x4F     | RightGUI    |
| 0x50     | LeftArrow      | 0x51     | RightArrow     | 0x52     | UpArrow       | 0x53     | DownArrow   |
| 0x54     | NumLock        | 0x55     | Keypad /       | 0x56     | Keypad *      | 0x57     | Keypad -    |
| 0x58     | Keypad +       | 0x59     | Keypad Enter   | 0x5A     | Keypad 1      | 0x5B     | Keypad 2    |
| 0x5C     | Keypad 3       | 0x5D     | Keypad 4       | 0x5E     | Keypad 5      | 0x5F     | Keypad 6    |
| 0x60     | Keypad 7       | 0x61     | Keypad 8       | 0x62     | Keypad 9      | 0x63     | Keypad 0    |
| 0x64     | Keypad .       | 0x65     | Media Play     | 0x66     | Media Pause   | 0x67     | Media Stop  |
| 0x68     | Media Eject    | 0x69     | Media Record   | 0x6A     | Media Next    | 0x6B     | Media Prev  |
| 0x6C     | Media Mute     | 0x6D     | Volume Up      | 0x6E     | Volume Down   | 0x6F     | BrightnessUp|
| 0x70     | BrightnessDown | 0x71     | Scroll Lock    | 0x72     | SysReq        | 0x73     | Cancel      |
| 0x74     | Clear          | 0x75     | Prior          | 0x76     | Return        | 0x77     | Separator   |
| 0x78     | Out            | 0x79     | Oper           | 0x7A     | ClearAgain    | 0x7B     | CrSel       |
| 0x7C     | ExSel          | 0x7D     | LeftCtrl       | 0x7E     | RightCtrl     | 0x7F     | LeftShift   |
| 0xE0     | LeftCtrl       | 0xE1     | LeftAlt        | 0xE2     | RightShift    | 0xE3     | LeftControl |
| 0xE4     | RightCtrl      | 0xE5     | RightShift     | 0xE6     | RightAlt      | 0xE7     | RightGUI    |
| 0xE8     | Media Play     | 0xE9     | Media Pause    | 0xEA     | Media Record  | 0xEB     | Media FastForward|
| 0xEC     | Media Rewind   | 0xED     | Media Next     | 0xEE     | Media Prev    | 0xEF     | Media Stop  |
```
