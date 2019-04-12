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

We need a python library that supports BLE. Currently ev3dev includes pybluez ang gattlib buth it doesn't work with the micro:bit so I added [pygatt]()https://github.com/peplin/pygatt.

```
   sudo apt-get install python3-pip
   sudo pip3 install pexpect
   sudo pip3 install pygatt
```

it will take a while so be sure to have fresh batteries or a wall adapter charging a EV3 battery.

Now just transfer the [demo01.py](https://github.com/JorgePe/microbit/blob/master/demo01.py) python script to your EV3, connect a Medium Motor to port A and you should control the motor with short presses of Button A or B (longer presses will not work because they return different codes).

Just two notes about the script:

+ The micro:bit requires a connection of type random (it is the only BLE device I own where I have to set this option, had to dig into the pygatt source code to find it)
```
   device = adapter.connect('F5:91:E3:32:23:39',address_type=pygatt.BLEAddressType.random)
```
+ I had to use the LED Matrix handle instead of the UUID because pygatt complains that no characteristic is found that matches it. The handle is 0x27 but it can change with future versions of the firmware (you can check the actual handle with the Nordic nRF Connect App or with a tool like 'gatttool').

A [video](https://youtu.be/7sGR8Ce65QA) showing the above script running:
[![EV3 and micro:bit](https://66.media.tumblr.com/97e82bcb856c7ac19df3f3683e98ae88/tumblr_ppaise45aV1ws4ayp_1280.jpg)](https://youtu.be/7sGR8Ce65QA "EV3 and micro:bit")

The [writemsg1.py](https://github.com/JorgePe/microbit/blob/master/writemsg1.py) script shows how to use just the LED Matrix service to draw some squares and crosses (a very short video: https://youtu.be/AHGr_eLJYz0)

As you probably noticed in the video, the responsiveness to the buttons is bad. Yes, EV3 hasn't the faster processor of h world but the micro:bit BLE services also don't seem much fast. So how can this be useful?

I started using BLE gadgets as a way to get sensory data. With the EV3 that's a way to get extra sensors without additional connections, some times even sensors that aren't available in LEGO world. Most of the time, we don't need real time access to the data - 1 to 10 samples each second are usually enough. So how can we use the micro:bit for that?

For onboard sensors, like the buttons or the temperature sensor, there are already BLE services that expose that data. But since the micro:bit also has several GPIO pins available, we can also use external sensors and expose the data through the micro:bit' BLE UART Service.

I'll show how to use this to add a wireless ultrasonic distance sensor to the MINDSTORMS EV3:

The HC-SR04 ultrasonic sensor is quite common among Arduino users and can also be ![used with the micro:bit](http://www.teachwithict.com/hcsr045v.html). The Makecode online editor already has a 'sonar' extension for it so the resulting program is quite simple - just read the value from the sensor once per second, display the result on the LED matrix and also send it over BLE to whoever might be listening.

![Program](https://github.com/JorgePe/microbit/blob/master/makecode-ultrasonic-ble.png)

On the EV3 side we just need to connect to the micro:bit and then subscribe to the micro:bit BLE UART TX characteristic in indication mode so that everytime the micro:bit sends a new reading we will receive it.

The [ultrasonic-ble-speak-2.py](https://github.com/JorgePe/microbit/blob/master/ultrasonic-ble-speak-2.py) script makes just that, printing the distance in the EV3 display but also speaking it loud:
[![Micro:bit Ultrasonic Sensor and EV3](https://i9.ytimg.com/vi/gnZdKOMnr2E/mq2.jpg?sqp=CJy8weUF&rs=AOn4CLAfBCdQWLpNinD4KkZGjjiYK6Crxw)](https://youtu.be/gnZdKOMnr2E "Micro:bit Ultrasonic Sensor and EV3")
