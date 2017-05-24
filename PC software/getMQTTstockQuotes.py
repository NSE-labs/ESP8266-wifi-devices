import urllib.request
import googlefinance
import json
import paho.mqtt.client as mqtt
import time

print('Posting stock quotes from google Finance to MQTT...')

proxy_support=urllib.request.ProxyHandler({'http' : 'http://3.20.109.242:9400'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

stocks = {'Apple':'AAPL',
          'GE':'GE',
          'Google':'GOOG',
           'S&P 500':'.INX',
           '5-yr Treas':'INDEXCBOE:FVX',
           '10-yr Treas':'INDEXCBOE:TNX'}

symbols = sorted(stocks.values())

client = mqtt.Client()
client.connect("localhost")


while True:
    try:
        data = json.loads(googlefinance.request(symbols))
    except:
        print('Network error')

    for i in range(0, len(symbols)):
        outstr1 = data[i]['t'] + ' ' + data[i]['l']
        outstr2 = data[i]['c'] + ' ' + data[i]['cp'] + '%'
        client.publish("line1",payload=outstr1)
        client.publish("line2",payload=outstr2)
        client.loop()
        time.sleep(10)
    
