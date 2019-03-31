# microbit
Using micro:bit with the LEGO MINDSTORMS EV3

The [BBC micro:bit](https://en.wikipedia.org/wiki/Micro_Bit) is a small ARM-based embedded system designed for Education.
It has a few sensors, LEDs, buttons and GPIO pins and can be used through USB or Bluetooh Low Energy.

This is a quick demonstration of how we can use a LEGO MINDSTORMS EV3 to communicate with a micro:bit through BLE. Will just how to present something in the the LED Matrix and read the two buttons but is very easy to use all the onboard devices.

Requirements:
- a LEGO MINDSTORMS EV3
- a [micro:bit](https://microbit.org/)
- a microSD card with [ev3dev linux](https://www.ev3dev.org/)
- a USB BT 4.x dongle with BLE

We want to use BLE so we need to flash a program into the micro:bit that exposes the devices we need as gatt charecteristics. A couple of years ago this was somewhat confusing but as of today it is quite easy by using the the online [Makecode editor](https://makecode.microbit.org/#editor):

We just need to add the Bluetooh extension to have the required Bluetooth blocks and create a very simple program to activate the required BLE services when the micro:bit starts. For that we just need to add two blocks wo our initial "on start" block:

+ bluetooth led service
+ bluetooth button service

This is our "program":
![Program](https://github.com/JorgePe/microbit/blob/master/makecode-ble-01.png)

We also need to configure the micro:bit to accept BLE connections without pairing. This was very confusing a few years ago, but now it's just an option in the "Project Settings':

+ No Pairing Required: Anyone can connect via Bluetooth

![Project settings](https://github.com/JorgePe/microbit/blob/master/makecode-ble-02.png)


Just save the project and upload the '.hex' file to the micro:bit, it will start almost immediately to announce itself as a BLE device named 'BBC micro:bit [zuvat]'.

If you have Nordic nRF Connect App you can already control the LED Matrix or read the buttons' state with it.

[Lancaster University](https://lancaster-university.github.io/microbit-docs/resources/bluetooth/bluetooth_profile.html) has documented all the BLE characteristics so we know that we need 3 UUID's:

+ Button A ('e95dda90-251d-470a-a062-fa1922dfa9a8')
+ Button B ('e95dda91-251d-470a-a062-fa1922dfa9a8')
+ LED Matrix ('e95d7b77-251d-470a-a062-fa1922dfa9a8')

Now for the EV3 to make use of these BLE services it need to run ev3dev linux. I will assume that you already know how to install and configure ev3dev and then connect to your EV3 through ssh and activate Bluetooth so I just explain what to do after:

We need a python library that supports BLE. Currently ev3dev includes pybluez ang gattlib buth it doesn't work the micro:bit so I added [pygatt]()https://github.com/peplin/pygatt.

```
   sudo apt-get install python3-pip
   sudo pip3 install pexpect```
   sudo pip3 install pygatt
```

it will take a while so be sure to have fresh batteries or a wall adapter charging a EV3 battery.

Now just transfer the [demo01.py](https://github.com/JorgePe/microbit/blob/master/demo01.py) python script to your EV3, connect a Medium Motor to port A and you should control the motor with short presses of Button A or B (longer presses will not work because they return different codes).

Just a note about the script: I had to use the LED Matrix handle instead of the UUID because pygatt complains that no characteristic is found that matches it. The handle is 0x27 but it can change with future versions of the firmware (you can check the actual handle with the Nordic nRF Connect App or with a tool like 'gatttool').

