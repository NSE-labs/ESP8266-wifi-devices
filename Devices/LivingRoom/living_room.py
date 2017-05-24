import machine
import micropython
import time

import my_digital_pin
import my_ds18b20
import my_mqtt

micropython.alloc_emergency_exception_buf(100)

temp_topic = b'home/livingroom/temperature'
motion_topic = b'home/livingroom/motion1'
ip_topic = b'home/livingroom/ip'

broker = my_mqtt.Connection('LivingRoom')

broker.publish_my_ip(ip_topic)

motion_sensor = my_digital_pin.PinToWatch(pin_number=2)
temp_sensors = my_ds18b20.Sensors(pin_number=0)

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
    motion_sensor.check_pin(broker, motion_topic)
    time.sleep_ms(100)
