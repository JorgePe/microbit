#!/usr/bin/env python3

from ev3dev2.sound import Sound
import pygatt
from time import sleep
from binascii import hexlify

DELAY = 1.0

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    distance = int(value.decode("utf-8"))
    print("Dist = {0:.2f} m".format(distance/100) )
    sound.speak(value.decode("utf-8"))

adapter = pygatt.GATTToolBackend()
adapter.start()
sound = Sound()
sound.speak('Welcome to the E V 3 dev project!')

while True:
    try:
        print("Connecting...")
        device = adapter.connect('F5:91:E3:32:23:39', address_type=pygatt.BLEAddressType.random)
        print("Connected")
        break
    except pygatt.exceptions.NotConnectedError:
        print("Not connected")
        sleep(1)
        continue

while True:
    try:
        device.subscribe("6e400002-b5a3-f393-e0a9-e50e24dcca9e", callback=handle_data, indication=True)
        break
    except pygatt.exceptions.BLEError:
        print("unknown characteristic")

try:
    while True:
        sleep(DELAY)
except Exception as e:
    print(e)
except (KeyboardInterrupt, SystemExit):
    print("Kbd/SysX")
    adapter.stop()
finally:
    adapter.stop()

