import usocket as socket
import ustruct as struct
import machine
import utime
import my_ssd1306
from umqtt.simple import MQTTClient

i2c = machine.I2C(scl=machine.Pin(2), sda=machine.Pin(0))
oled = my_ssd1306.SSD1306_I2C(128, 64, i2c)

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

# bitmaps of 8x8 symbols
connected_char = [0x80, 0, 0xe0, 0, 0xf8, 0, 0xfe, 0]
error_char = [0x80, 0xe0, 0xf8, 0x46, 0xf8, 0xe0, 0x80, 0]

daystr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
lineypos = [0, 16, 32, 42]

line1 = ''
line2 = ''

def getNTPtime(host):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    try:
        addr = socket.getaddrinfo(host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        val -= NTP_DELTA
    except:
        val = 0
    return val

# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
def settime():
    t = getNTPtime('192.168.4.2')
    if t==0:
        return True # If an error occurred return an errorflag of True and don't set the time
    t -= 21600      # Correct for timezone - 6 hours for CST
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    return False    # no error occurred

def show_symbol(bitmap, offset):    # show an 8x8 bitmap at byte offset specified
    for x in range(0, 8):
        oled.set_byte(offset, bitmap[x])
        offset += 1

def updateDisplay(curtime, errorflag):
    timestr = str(curtime[3])+':'+'{0:0>2}'.format(curtime[4])+':'+'{0:0>2}'.format(curtime[5])
    datestr = daystr[curtime[6]]+' '+str(curtime[1])+'/'+str(curtime[2])+'/'+str(curtime[0])
    oled.fill(0)
    line = 0
    for s in (timestr, datestr, line1, line2):
        xpos = 64-(len(s)*4)    # Center the string which has variable length 
        oled.text(s,xpos,lineypos[line])
        line += 1
    if errorflag:
        show_symbol(error_char, 0)
    else:
        show_symbol(connected_char, 0)   
    oled.show()

def sub_callback(topic, msg):
    global line1, line2
    if topic==b'line1':
        line1 = msg
    elif topic == b'line2':
        line2 = msg

c = MQTTClient("ESP8266", "192.168.4.2")
c.set_callback(sub_callback)

try:
    c.connect()
    c.subscribe("line1")
    c.subscribe("line2")
except:
    line1 = 'No MQTT server'
    line2 = 'reset to retry'
    
errorflag = settime()
prevsecond = 0
while True:
    curtime = utime.localtime()
    if curtime[5] != prevsecond:    # if the seconds number has changed
        prevsecond = curtime[5]
        # Get the NTP time every 15 minutes (minute%15 == 0 and seconds == 0)
        # or if the last attempt failed (errorflag is True) try again every minute (seconds == 0)
        if (curtime[4]%15 == 0 or errorflag) and curtime[5] == 0:
            errorflag = settime()
        updateDisplay(curtime, errorflag)
    try:
        c.check_msg()
    except:
            line1 = 'No MQTT server'
            line2 = 'reset to retry'
        
    utime.sleep_ms(250)
