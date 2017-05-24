import dht
from umqtt.simple import MQTTClient
import machine
import time

sensor = dht.DHT22(machine.Pin(2))
client = MQTTClient("ESP8266", "192.168.1.32")

time.sleep(3)   # allow sensor to initialize

while True:
    connected = False
    while not connected:
        try:    
            client.connect()
            connected = True
        except (KeyboardInterrupt, SystemExit):
           raise 
        except:
            print('Failed connection')
    try:
        while True:
            sensor.measure()    # start a measurement
            time.sleep(5)
            sensor.measure()    # read the results
            tempC = sensor.temperature()
            tempF = (tempC * 1.8) + 32 
            client.publish(b'Temperature1', b'{:.1f}'.format(tempF))
            client.publish(b'Humidity1', b'{:.1f}'.format(sensor.humidity()))
            time.sleep(55)      # 60 seconds minus 5 second measurement time
    except (KeyboardInterrupt, SystemExit):
        raise 
    except:
        print('Failed to publish')
