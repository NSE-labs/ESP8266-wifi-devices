# This file is executed on every boot (including wake-boot from deepsleep)

from machine import Pin

p = Pin(2, Pin.OUT, value=1)

import my_network

my_network.connect()
