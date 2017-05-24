import machine
import micropython
import time

import my_ds18b20
import my_mqtt

micropython.alloc_emergency_exception_buf(100)

temp_topic = b'office/temperature'
ip_topic = b'office/ip'

broker = my_mqtt.Connection('Office')

broker.publish_my_ip(ip_topic)

temp_sensors = my_ds18b20.Sensors(pin_number=2)

timeout = True


def set_timeout(dummy):
    global timeout
    timeout = True


t = machine.Timer(-1)
t.init(period=60000, mode=machine.Timer.PERIODIC, callback=set_timeout)

while True:
    if timeout:
        temp_sensors.publish_temps(broker, temp_topic)
        timeout = False
    time.sleep_ms(100)
