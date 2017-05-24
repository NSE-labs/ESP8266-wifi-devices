import machine
import onewire
import ds18x20
import time

'''
This class can handle any number of DS18B20 temperature sensors attached
to a single pin
'''


class Sensors:
    def __init__(self, pin_number):
        ow = onewire.OneWire(machine.Pin(pin_number))
        self.ds = ds18x20.DS18X20(ow)
        self.roms = self.ds.scan()
        print(len(self.roms), 'sensors found')

    def publish_temps(self, broker, topic):
        self.ds.convert_temp()
        time.sleep_ms(750)
        for index, rom in enumerate(self.roms):
            temp_f = (self.ds.read_temp(rom)*1.8) + 32
            broker.publish(topic + b'{}'.format(index+1),
                           b'{:.1F}'.format(temp_f))
