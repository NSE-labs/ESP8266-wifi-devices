import time
import network

wifiAPs = [('AP', 'password'),
           ('NSE', 'experiment')]


def wifi_connect(sta_if, ssid, password):
    sta_if.connect(ssid, password)
    for i in range(15):    # time out after 15 seconds if not connected
        if sta_if.isconnected():
                return True
        time.sleep(1)
    return False


def connect():
    access_pt = network.WLAN(network.AP_IF)
    station = network.WLAN(network.STA_IF)
    if station.isconnected():
        return station.ifconfig()[2]
    print('Connecting to network...')
    station.active(True)
    for (ssid, password) in wifiAPs:
        print('Trying', ssid)
        if wifi_connect(station, ssid, password):
            access_pt.active(False)  # turn off access point
            print('network config:', station.ifconfig())
            return station.ifconfig()[2]
        print('Could not connect to', ssid)
    print('No wifi available, becoming an access point')
    station.active(False)
    access_pt.active(True)
    print('network config:', access_pt.ifconfig())
    return access_pt.ifconfig()[2]
