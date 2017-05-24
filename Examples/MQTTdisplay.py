from umqtt.simple import MQTTClient
import machine
import ssd1306

i2c = machine.I2C(scl=machine.Pin(2), sda=machine.Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def sub_callback(topic, msg):
    # scroll up one line
    for i in range(10):
        oled.scroll(0, -1)
        oled.show()
    # show the received message on the display    
    oled.text(msg,0,55)
    oled.show()

c = MQTTClient("ESP8266", "192.168.4.2")
c.set_callback(sub_callback)
c.connect()
c.subscribe("screen")
try:
    while True:
        c.wait_msg()
finally:
    c.disconnect()
