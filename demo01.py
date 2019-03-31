#!/usr/bin/env python3

import pygatt
from time import sleep
import ev3dev.ev3 as ev3

adapter = pygatt.GATTToolBackend()
m = ev3.MediumMotor('outA')

DELAY = 0.1

try:
    adapter.start()
    device = adapter.connect('F5:91:E3:32:23:39',address_type=pygatt.BLEAddressType.random)

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

    while True:
        buttonA = device.char_read("e95dda90-251d-470a-a062-fa1922dfa9a8")
        buttonB = device.char_read("e95dda91-251d-470a-a062-fa1922dfa9a8")

        if buttonA == bytearray(b'\x01'):
            device.char_write_handle(0x27, bytearray([0x04, 0x08, 0x10, 0x08, 0x04]))
            m.run_timed(time_sp=100, speed_sp=-500)
        elif buttonB == bytearray(b'\x01'):
            device.char_write_handle(0x27, bytearray([0x04, 0x02, 0x01, 0x02, 0x04]))
            m.run_timed(time_sp=100, speed_sp=500)
        else:
            device.char_write_handle(0x27, bytearray([0x00, 0x00, 0x00, 0x00, 0x00]))

        sleep(0.1)

finally:
    adapter.stop()

