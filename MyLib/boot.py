# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import webrepl

import my_network


my_network.connect()
webrepl.start()
gc.collect()
