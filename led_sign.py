import Weather
import time
import urllib2
from httplib2 import Http
import random
import json
import socket

btcguild = "https://www.btcguild.com/api.php?api_key=cf2ca3cf591ae16ba923fcf857c6f6ee"
coinbase = "https://coinbase.com/api/v1/currencies/exchange_rates"
miner = "192.168.1.143"
minerPort = 4028

req = urllib2.Request(btcguild, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"})
data = urllib2.urlopen(req).read()
p = json.loads(data)
earned = p["user"]["past_24h_rewards"]
total = p["user"]["total_rewards"]

req = urllib2.Request(coinbase, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"})
data = urllib2.urlopen(req).read()
p = json.loads(data)
value = p["btc_to_usd"]
earned_usd = float(value) * float(earned)
earnedString = str(round(earned_usd,2))
coinsString = str(earned*1000)
mBTC = total*1000
mBTCString = str(mBTC)
total_usd = float(value) * float(total)
totalString = str(round(total_usd,2))

# HOLY FUCKING SHIT I GOT IT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((miner, minerPort))
s.send("{\"command\":\"summary\"}")

sData = ''

while True:
    newdata = s.recv(1024)
    if newdata:
        sData += newdata
    else:
        break

s.close()

if sData:
    p = json.loads(sData.replace('\x00',''))
    uptime = p["SUMMARY"][0]["Elapsed"]
    days = int(uptime/86400)
    if days == 1:
	dayString = "Day"
    else:
	dayString = "Days"
    hours = time.strftime('%H:%M:%S', time.gmtime(uptime))
    formatTime = str(days) + " " +  dayString + " " + hours

# Instantiate our shits
h = Http()
w = Weather.Station('KBZN')
bros = ['dude', 'bro', 'man', 'dawg', 'guy']

# Define what shit we do
def led_sign_weather_print():
    w.update()
    tempF = w['temp_f']
    tempC = w['temp_c']
    broString = "<FE> It's " + str(tempF) + " F   (" + str(tempC) + "C) outside, " + random.choice(bros) + " "
    print time.asctime()
    datString = broString + "at " + time.asctime() + " and we earned <FL><CM>\$"  + earnedString + " mining<CG><FR>" + coinsString + " mBTC <CP>today, for a total of <FN><CD>" + mBTCString + " mBTC  valued at <CM>\$" + totalString + "    <CP>Uptime on the miner is " + formatTime + "  <FF>"
    print datString
    formatedOutput = urllib2.quote(datString)
    finalOutput = "http://localhost:1337/sign.php?textToPost=" + formatedOutput
    resp, content = h.request(finalOutput, "POST")
    time.sleep(2)
    resp, content = h.request(finalOutput, "POST")

led_sign_weather_print()
