#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import sys, time, json, string, cgi, subprocess, json, datetime, memcache
import settings as settings
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# get the temp and conditions for candle to reflect changes, sets to memcache for candle to read
count = 0
while count < 10:
    try:
        count = count + 1        
        weatherInfo = json.loads(subprocess.check_output(['curl', settings.weatherAPIURL ]))
        currentFeelsLikeTemp = weatherInfo['currently']['apparentTemperature']
        
        # get the color for the current temp and set the jar to glow in that color
        colorInfo = subprocess.check_output(['curl', settings.tempColorAPI + '/neopixel?temperature=' + str(int(currentFeelsLikeTemp))   ])
        mc.set("TEMPERATURE", str(colorInfo))
        
        #weatherInfo['currently']['precipProbability'] = 1
  
        # @TODO
        # if the temp is in the "white" color range  it should be brighter blinking
        # get the snow / rain conditions working
        # get the wind conditions working
        # if there's no special condition, then just "NONE"
        
        mc.set("CONDITIONS", "NONE")

        break
    except (Exception):
        time.sleep(10)



