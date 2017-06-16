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
    """
    If already connected as a station, return

    Configure as an access point and start a web server
    to allow configuration from a browser.

    After a timeout period with no web configuration activity
      If a valid configuration exists
        Connect to the configured network
          If able to connect to configured network
            Turn off web server and access point and return
          Else if unable to connect to configured network
            Start the whole process again
      Else if no configuration exists
        Stay as access point to allow web configuration
    """
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
