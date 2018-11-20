#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess, json, datetime
import settings as settings
from neopixel import *

# LED strip configuration:import settings as settings
LED_COUNT      = 24     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

############################################
######## YOU HAVE TO RUN AS ROOT!
############################################

# setup the strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, ws.WS2811_STRIP_GRB)
strip.begin()

def hexToRGB(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def precipIndicator(strip, iteration):
    strip.setPixelColor(11, Color(iteration, iteration, iteration))
    strip.show()

def fadeIn(strip, speed):
    count = 0
    while count < 250:
        count = count + 10
        precipIndicator(strip, count)
        time.sleep(speed)

def fadeOut(strip, speed):
    count = 250
    while count > 0:
        count = count - 10
        precipIndicator(strip, count)
        time.sleep(speed)

# get the temp and conditions at sunrise and conditions for the day (try 10 times in case of network outage other errors)
count = 0
while count < 10:
    try:
        count = count + 1        
        weatherInfo = json.loads(subprocess.check_output(['curl', weatherAPIURL + settings.weatherAPIKey + '/' + str(currentLocationInfo['latitude']) + ',' + str(currentLocationInfo['longitude']) + '?lang=en']))
        currentFeelsLikeTemp = weatherInfo['currently']['apparentTemperature']
        break
    except (Exception):
        time.sleep(10)

# get the color for the current temp and set the jar to glow in that color
colorInfo = subprocess.check_output(['curl', tempColorAPI + '/neopixel?temperature=' + str(int(currentFeelsLikeTemp))   ])
rgbValue = hexToRGB(colorInfo)
for i in range(0, strip.numPixels(), 4):
    strip.setPixelColor(i, Color(rgbValue[0], rgbValue[1], rgbValue[2]))
strip.show()

# if currently active precip, then show fading light 
if weatherInfo['currently']['precipProbability'] == 1:
    count = 0
    while count < 100:
        count = count + 1
        fadeIn(strip, 0.01)
        fadeOut(strip, 0.01)
