import machine
import micropython
import time

import my_ds18b20
import my_mqtt
import my_digital_pin

micropython.alloc_emergency_exception_buf(100)

temp_topic = b'home/garage/temperature'
ip_topic = b'home/garage/ip'
door1_topic = b'home/garage/door1open'
door2_topic = b'home/garage/door2open'

broker = my_mqtt.Connection('Garage')

broker.publish_my_ip(ip_topic)

temp_sensors = my_ds18b20.Sensors(pin_number=2)

timeout = True


def set_timeout(dummy):
    global timeout
    timeout = True


t = machine.Timer(-1)
t.init(period=60000, mode=machine.Timer.PERIODIC, callback=set_timeout)

door1 = my_digital_pin.PinToWatch(pin_number = 14, pull_up=True)
door2 = my_digital_pin.PinToWatch(pin_number = 12, pull_up=True)

while True:
    if timeout:
        temp_sensors.publish_temps(broker, temp_topic)
        door1.publish_pin(broker, door1_topic)
        door2.publish_pin(broker, door2_topic)
        timeout = False
    door1.check_pin(broker, door1_topic)
    door2.check_pin(broker, door2_topic)
    time.sleep_ms(100)
