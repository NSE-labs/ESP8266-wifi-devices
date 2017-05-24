import my_mqtt

press_topic = b'home/button1/press'
ip_topic = b'home/button1/ip'

broker = my_mqtt.Connection('Button1')

broker.publish(press_topic, b'Pressed', retain_it=False)

broker.publish_my_ip(ip_topic)

broker.disconnect()

import time
time.sleep(1)

import machine
p = machine.Pin(2, machine.Pin.OUT, value=0)  # turn off chip enable

time.sleep(5)

# if we get here then someone is holding the button, preventing shutdown
# so don't shut down and turn on gc and webrepl
p.value(1)  # assert chip enable
import gc
import webrepl
webrepl.start()
gc.collect()

time.sleep(60)  # give the user 60 seconds to connect and hit ctrl-C

p.value(0)  # otherwise turn off CE and reset - go back to being a button

while True:  # loop forever waiting to reset
    pass
