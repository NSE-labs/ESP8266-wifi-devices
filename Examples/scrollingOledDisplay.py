
import machine
import ssd1306

i2c = machine.I2C(scl=machine.Pin(2), sda=machine.Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

line=['Oled display',
      '128x64 pixels',
      'ESP8266 CPU',
      'WiFi enabled',
      'Micropython',
      'Dev Brd $8.79',
      'Display $9.99']

while True:
    for j in range(len(line)):
        for i in range(16):
            oled.scroll(0, -1)
            oled.show()

        oled.text(line[j],0,48)
        oled.show()

