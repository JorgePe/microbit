#!/usr/bin/env python3

import pygatt
from time import sleep

DELAY=0.1

adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    device = adapter.connect('F5:91:E3:32:23:39',address_type=pygatt.BLEAddressType.random)
    while True:
        device.char_write_handle(0x27, bytearray([0x1F, 0x11, 0x11, 0x11, 0x1F]))
        sleep(DELAY)
        device.char_write_handle(0x27, bytearray([0x00, 0x0E, 0x0A, 0x0E, 0x00]))
        sleep(DELAY)
        device.char_write_handle(0x27, bytearray([0x00, 0x00, 0x04, 0x00, 0x00]))
        sleep(DELAY)
        device.char_write_handle(0x27, bytearray([0x00, 0x00, 0x00, 0x00, 0x00]))
        sleep(DELAY)
        device.char_write_handle(0x27, bytearray([0x11, 0x0A, 0x04, 0x0A, 0x11]))
        sleep(DELAY)
        device.char_write_handle(0x27, bytearray([0x00, 0x0A, 0x04, 0x0A, 0x00]))
        sleep(DELAY)
        device.char_write_handle(0x27, bytearray([0x00, 0x00, 0x04, 0x00, 0x00]))
        sleep(DELAY)
        device.char_write_handle(0x27, bytearray([0x00, 0x00, 0x00, 0x00, 0x00]))
        sleep(DELAY)
finally:
    adapter.stop()

