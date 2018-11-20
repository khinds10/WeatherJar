#!/usr/bin/python
import os, sys, re, json
from flask import Flask
from flask import request
from PIL import Image
app = Flask(__name__)
dirPath = os.path.dirname(os.path.realpath(__file__))

def rgbOfPixel(img_path, x, y):
    """for given image path, get the color at the x,y coords"""
    im = Image.open(img_path).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r, g, b)
    return a

def getHexForColor(temperature, gradientImageFile):
    """get HEX code for given color"""    
    try:    
        temperature = temperature * 10
        if temperature > 999:
            temperature = 999
        if temperature < 0:
            temperature = 0
        color = rgbOfPixel(dirPath + gradientImageFile, temperature, 5)
        return '#%02x%02x%02x' % color
    except:
        return '#ffffff'

@app.route("/neopixel")
def getTemperatureColor():
    """get temperature to generate the HEX color for neopixel color scheme"""
    temperature = int(request.args.get('temperature'))
    return getHexForColor(temperature, '/neopixel.png')
        
# run the flask python API
if __name__ == "__main__":
    app.run()
