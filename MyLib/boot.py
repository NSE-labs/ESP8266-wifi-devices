# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import webrepl
import micropython

import my_network

micropython.alloc_emergency_exception_buf(100)
my_network.connect()
webrepl.start()
gc.collect()
