"""
sonoff.py
Replacement code for the Sonoff switch

Register for the command topic
If command topic payload is "ON", turn the switch on, else turn the switch off
If user presses the button on the Sonoff, toggle the on/off state
Send current state in the state_topic
Always keep the LED in sync with the on/off state

The pin functions of the Sonoff are:
GPIO 0 - Button (active low)
GPIO 12 - Relay (active high)
GPIO 13 - LED (active low)
"""

import machine
import micropython
import time

import my_mqtt

micropython.alloc_emergency_exception_buf(100)

ON = 1
OFF = 0
BUTTON_PIN = 0
RELAY_PIN = 12
LED_PIN = 13
IP_TOPIC = b'home/switch2/ip'
STATE_TOPIC = b'home/switch2/state'
COMMAND_TOPIC = 'home/switch2/set'

relay = machine.Pin(RELAY_PIN, machine.Pin.OUT)
relay.value(0)  # relay off
led = machine.Pin(LED_PIN, machine.Pin.OUT)
# flash the LED
led.value(0)    # LED on
time.sleep(1)
led.value(1)    # LED off



broker = my_mqtt.Connection('Switch2')
broker.publish_my_ip(IP_TOPIC)

switch_state = OFF


def set_switch(new_switch_state):
    global switch_state
    switch_state = new_switch_state
    relay.value(switch_state)
    led.value(1 - switch_state)
    if switch_state:
        broker.publish(STATE_TOPIC, b'ON')
    else:
        broker.publish(STATE_TOPIC, b'OFF')


def mqtt_callback(topic, msg):
    if topic == bytes(COMMAND_TOPIC, "utf-8"):
        if msg == b'ON':
            set_switch(ON)
        else:
            set_switch(OFF)


broker.set_callback(mqtt_callback)
broker.subscribe(COMMAND_TOPIC)

button = machine.Pin(BUTTON_PIN, machine.Pin.IN)
last_button_state = 0

while True:
    button_state = button.value()
    if button_state != last_button_state:
        if last_button_state == 1:      # button pressed when it wasn't before
            if switch_state:            # toggle the switch state
                set_switch(OFF)
            else:
                set_switch(ON)
        last_button_state = button_state
    broker.check_msg()
    time.sleep_ms(100)
