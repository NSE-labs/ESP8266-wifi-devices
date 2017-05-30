# ESP8266-wifi-devices
Micropython code for various ESP8266-based sensor, switching, and display devices used in home automation. The directory organization is generally according to where the device is located, although in the case of the Sonoff switch it is by function, since these switches are used in several locations.

## Devices directory
### Devices/Bedroom
This device is based on the Node MCU ESP8266 module with the following components attached:
- A LED that is pulse-width modulated for brightness attached to GPIO14 (D5 on the Node MCU module)
- A DHT22 temperature and humidity sensor attached to GPIO0 (D3)
- A binary motion sensor attached to GPIO2 (D4)
- A binary light sensor attached to GPIO12 (D6)

### Devices/Button
This device is designed to be battery powered. It is based on an ESP-01 module that has been modified to remove the red power LED to reduce current draw. When the attached button is pressed, the CPU wakes up, connects to the network, and sends an MQTT message saying the button was pressed. It then goes back to sleep to save battery life. If the button is held continuously for more than about 10 seconds, the CPU stays on for 60 more seconds and you can connect to the WebREPL to debug or reprogram the device (once you connect to WebREPL you must hit ctrl-C to stop the running program before the 60 seconds is up). An attached LED is lit while the CPU is awake.

### Devices/Garage
This device is based on the Node MCU module with the following sensors:
- A DS18B20 temperature sensor attached to GPIO2 (D4)
- Two binary magnetic door sensors to indicate when two garage doors are open/closed. These are attached to GPIO14 (D5) and GPIO12 (D6)

### Devices/Lab
This is very similar to the Bedroom sensor, except the message topics were changed to indicate the Lab location.

### Devices/LivingRoom
This is based on the ESP-01 module with:
- A DS18B20 temperature sensor attached to GPIO0
- A binary motion sensor attached to GPIO2

### Devices/Office
This is based on the ESP-01 module with a single DS18B20 temperature sensor attached to GPIO2.

### Devices/Sonoff
This is software to reprogram the commercially available Sonoff switch to allow MQTT messaging.

## Examples directory
Contains some experimental programs to test interfaces to various components.

## MyLib directory
Contains various python modules used in the programs in the Devices directory.

## PC software directory
Contains a support program that runs on a PC to get stock market quotes and send them as MQTT messages.

## Tools directory
Contains a Microsoft Excel spreadsheet to help develop special characters for a bitmap display.
