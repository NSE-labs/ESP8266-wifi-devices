import machine
import onewire
import ds18x20
import time
from umqtt.simple import MQTTClient

c = MQTTClient("ESP8266-2", "192.168.4.2")
c.connect()
ow = onewire.OneWire(machine.Pin(0))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
print(len(roms),'sensors found')
timeout = True

def publishTemps():
    ds.convert_temp()
    time.sleep_ms(750)
    for i,rom in enumerate(roms):
        tempF = (ds.read_temp(rom)*1.8) + 32
        c.publish(b'Temp{}'.format(i), b'{:.2F}'.format(tempF))

def setTimeout(dummy):
    global timeout
    timeout = True

t = machine.Timer(-1)
t.init(period=60000, mode=machine.Timer.PERIODIC, callback=setTimeout)

motionPin = machine.Pin(2, machine.Pin.IN)
laststate = 0
while True:
    if timeout:
        publishTemps()
        timeout = False
    curstate = motionPin.value()
    if laststate != curstate:
        c.publish(b'Motion0', b'{}'.format(curstate))
        laststate = curstate
