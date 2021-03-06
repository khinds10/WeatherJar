#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import sys, time, json, string, cgi, subprocess, json, datetime, memcache
import settings as settings
from neopixel import *
from random import *
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# rain raindrops timeout length (generated randomly) 
rainDrops = ['0.1', '0.2', '0.3', '0.4', '0.8', '0.9']

# wind speed timeout length (generated randomly) 
windSpeed = ['0.02', '0.03', '0.04', '0.05', '0.06', '0.07', '0.08']

# LED strip configuration:import settings as settings
LED_COUNT      = 16     # Number of LED pixels.
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

# set all pixels to black
for i in range(0, strip.numPixels()):
    strip.setPixelColor(i, Color(0, 0, 0))
strip.show()

def hexToRGB(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def setEventPin(pin, brightness, speed):
    global strip
    strip.setPixelColor(pin, Color(brightness, brightness, brightness))
    strip.show()
    time.sleep(speed)

def turnOnOff(pin, brightness, speed):
    global strip
    setEventPin(pin, brightness, speed)
    setEventPin(pin, 0, speed)

def getDrop():
    """get random raindrop length for effect"""
    global rainDrops
    shuffle(rainDrops)
    return float(rainDrops[0])

def getGust():
    """get random wind gust length for effect"""
    global windSpeed
    shuffle(windSpeed)
    return float(windSpeed[0])

def rain(temperatureColor):
    """rain blinking effect"""    
    # make the effect more pronounced for when the candle is already white
    rainBrightness = 50
    if temperatureColor == "#ffffff":
        rainBrightness = 100
    turnOnOff(2, rainBrightness, getDrop())
    turnOnOff(3, rainBrightness, getDrop())
    turnOnOff(7, rainBrightness, getDrop())
    turnOnOff(11, rainBrightness, getDrop())
    
def wind(temperatureColor):
    """wind faster blinking effect"""
    # make the effect more pronounced for when the candle is already white
    windBrightness = 25
    if temperatureColor == "#ffffff":
        windBrightness = 50
    turnOnOff(2, windBrightness, getGust())
    turnOnOff(3, windBrightness, getGust())
    turnOnOff(7, windBrightness, getGust())
    turnOnOff(11, windBrightness, getGust())
    
def snow(temperatureColor):
    """snow fading effect"""
    count = 0
    while count < 255:
        count = count + 1
        setEventPin(11, count, 0.005)
    while count > 0:
        count = count - 1
        setEventPin(11, count, 0.005)

# run the candle infinitely, getting the current temp and conditions
while True:
    try:
        temperatureColor = mc.get("TEMPERATURE")
        rgbValue = hexToRGB(temperatureColor)
        for i in range(0, strip.numPixels(), 4):
            strip.setPixelColor(i, Color(rgbValue[0], rgbValue[1], rgbValue[2]))
        strip.show()
        conditions = mc.get("CONDITIONS")
        if conditions == "RAIN":
            rain(temperatureColor)
        if conditions == "WIND":
            wind(temperatureColor)
        if conditions == "SNOW":
            snow(temperatureColor)
    except (Exception):
        time.sleep(1)
