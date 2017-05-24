import network
import time

from umqtt.simple import MQTTClient

import my_network


class Connection:
    def __init__(self, client_name):
        self.client_name = client_name
        self.subscriptions = []  # create an empty list to hold subscriptions
        self.callback = False    # keep track of the callback if one is set
        self.initialize()

    def initialize(self):
        connected = False
        while not connected:
            self.gateway = self.check_network()
            self.broker = self.get_broker(self.gateway)
            self.client = MQTTClient(self.client_name, self.broker)
            connected = self.connect_to_broker(self.client)

    def check_network(self):
        station = network.WLAN(network.STA_IF)
        access_pt = network.WLAN(network.AP_IF)
        if station.isconnected():
            return station.ifconfig()[2]
        elif access_pt.isconnected():
            return access_pt.ifconfig()[2]
        else:
            print('No network connection, waiting to retry...')
            time.sleep(120)  # Wait 2 minutes before trying to reconnect
            print('Reconnecting to network...')
            return my_network.connect()

    def get_broker(self, gateway):
        # MQTT broker ip address based on gateway ip address
        brokers = {'192.168.1.1': '192.168.1.32',
                   '192.168.40.1': '192.168.40.1',
                   '192.168.4.1': '192.168.4.2'}
        if gateway in brokers:
            return brokers[gateway]
        else:  # default
            return '192.168.1.32'

    def connect_to_broker(self, client):
        for i in range(3):
            try:
                client.connect()
            except (KeyboardInterrupt, SystemExit):
                raise
            except OSError as e:
                print('Failed connection to broker:', e)
                time.sleep(5)
                print('Retrying...')
            else:
                print('Connected to broker', self.broker)
                if self.callback:
                    print('Reinitializing callback')
                    self.set_callback(self.callback)
                for topic in self.subscriptions:
                    print('Resubscribing to', topic)
                    self.client.subscribe(topic)
                return True
        print('Unable to connect to broker')
        return False

    def subscribe(self, topic):
            self.subscriptions.append(topic)  # keep a list of subscriptions
            self.client.subscribe(topic)

    def set_callback(self, function):
            self.callback = function
            self.client.set_callback(function)

    def publish(self, topic, msg, retain_it=False):
        try:
            self.client.publish(topic, msg, retain=retain_it)
        except OSError as e:
            print(e, '\nFailed to publish, reconnecting...')
            self.initialize()

    def check_msg(self):
        try:
            self.client.check_msg()
        except OSError as e:
            print(e, '\nCheck message error, reconnecting...')
            self.initialize()

    def publish_my_ip(self, topic):
        station = network.WLAN(network.STA_IF)
        if station.isconnected():
            self.publish(topic, station.ifconfig()[0], retain_it=True)

    def disconnect(self):
        self.client.disconnect()
