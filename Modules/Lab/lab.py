import dht
import machine
import micropython
import time

import my_mqtt
import my_digital_pin

micropython.alloc_emergency_exception_buf(100)

led1_cmd_topic = 'home/lab/led1/cmd'
led1_state_topic = b'home/lab/led1/state'
led1_brightness_cmd_topic = 'home/lab/led1/brightcmd'
led1_brightness_state_topic = b'home/lab/led1/brightstate'
temp_topic = b'home/lab/temperature1'
humidity_topic = b'home/lab/humidity1'
motion_topic = b'home/lab/motion1'
light_sensor_topic = b'home/lab/lightsensor1'
ip_topic = b'home/lab/ip'

broker = my_mqtt.Connection('Lab')

broker.publish_my_ip(ip_topic)

led1 = machine.PWM(machine.Pin(14), freq=1000, duty=0)
led1_brightness = 0
led1_state = 'OFF'
broker.publish(led1_state_topic, b'OFF')
broker.publish(led1_brightness_state_topic, b'0')


def mqtt_callback(topic, msg):
    global led1_brightness, led1_state
    if topic == bytes(led1_brightness_cmd_topic, "utf-8"):
        try:
            brightness = int(msg)
        except ValueError:  # the string msg is not a valid number
            brightness = 0
        if brightness > 100:
            brightness = 100
        elif brightness < 0:
            brightness = 0
        if led1_state == 'ON':
            led1.duty(brightness*10)
        led1_brightness = brightness
        broker.publish(led1_brightness_state_topic, b'{}'.format(brightness))
    elif topic == bytes(led1_cmd_topic, "utf-8"):
        if msg == b'ON':
            led1_state = 'ON'
            led1.duty(led1_brightness * 10)
            broker.publish(led1_state_topic, b'ON')
        elif msg == b'OFF':
            led1_state = 'OFF'
            led1.duty(0)
            broker.publish(led1_state_topic, b'OFF')


broker.set_callback(mqtt_callback)
broker.subscribe(led1_cmd_topic)
broker.subscribe(led1_brightness_cmd_topic)

sensor = dht.DHT22(machine.Pin(0))


def do_dht22():
    sensor.measure()    # start a measurement
    time.sleep(5)
    sensor.measure()    # read the results
    temp_c = sensor.temperature()
    temp_f = (temp_c * 1.8) + 32
    broker.publish(temp_topic, b'{:.1f}'.format(temp_f))
    broker.publish(humidity_topic, b'{:.1f}'.format(sensor.humidity()))


timeout = True


def set_timeout(dummy):
    global timeout
    timeout = True


t1 = machine.Timer(-1)
t1.init(period=60000, mode=machine.Timer.PERIODIC, callback=set_timeout)

time.sleep(3)   # allow sensors to initialize

motion_sensor = my_digital_pin.PinToWatch(pin_number=2)
light_sensor = my_digital_pin.PinToSample(pin_number=12)

while True:
    if timeout:
        do_dht22()
        light_sensor.publish_pin(broker, light_sensor_topic, invert=True)
        timeout = False
    motion_sensor.check_pin(broker, motion_topic)
    broker.check_msg()
    time.sleep_ms(100)
