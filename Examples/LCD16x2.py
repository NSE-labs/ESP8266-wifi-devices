from umqtt.simple import MQTTClient
import machine
import utime

line1 = bytearray(16)
line2 = bytearray(16)

class lcdDisplay:
    def __init__(self):
        self.i2c = machine.I2C(scl=machine.Pin(2), sda=machine.Pin(0), freq=20000)
        self.i2cAddress = 40    # I2C address of the LCD module
        self.turnDisplayOn()
        self.setBrightness(4)
        self.clearScreen()

    def turnDisplayOn(self):
        self.i2c.writeto(self.i2cAddress, b'\xFE\x41')


    def setBrightness(self, brightness):
        # brightness range is 1-8
        if brightness < 1:
            brightness = 1
        elif brightness > 8:
            brightness = 8
        buf = bytearray(b'\xFE\x53\x01')
        buf[2] = brightness
        self.i2c.writeto(self.i2cAddress, buf)

 
    def clearScreen(self):
        self.i2c.writeto(self.i2cAddress, b'\xFE\x51')


    def writeText(self, text, cursor_pos=0):
        buf = bytearray(b'\xFE\x45\x00')
        buf[2] = cursor_pos
        self.i2c.writeto(self.i2cAddress, buf)  # set cursor position
        self.i2c.writeto(self.i2cAddress, text) # write the text


lcd = lcdDisplay()

def sub_callback(topic, msg):
    global line1, line2
    if topic==b'line1':
        line1=b'{0: <16}'.format(msg)   # pad with spaces
        lcd.writeText(line1, 0)
    elif topic == b'line2':
        line2=b'{0: <16}'.format(msg)   # pad with spaces
        lcd.writeText(line2, 64)        # position at beginning of second line
        

c = MQTTClient("ESP8266", "192.168.4.2")
c.set_callback(sub_callback)

try:
    c.connect()
    c.subscribe("line1")
    c.subscribe("line2")    
except:
    lcd.writeText('No MQTT server  ', 0)
    lcd.writeText('reset to retry  ', 0)

while True:
    c.wait_msg()

    
