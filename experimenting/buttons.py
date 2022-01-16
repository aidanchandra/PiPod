# Copyright (c) 2017 Adafruit Industries
# Author: James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


#import RPi.GPIO as GPIO

import time

#import Adafruit_GPIO.SPI as SPI
#import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



# Input pins:
L_pin = 27 
R_pin = 23 
C_pin = 4 
U_pin = 17 
D_pin = 22 

A_pin = 5 
B_pin = 6 

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
#disp.begin()

# Clear display.
#disp.clear()
#disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128#disp.width
height = 64#disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)


draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled
draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled
draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
draw.rectangle((20, 22,40,40), outline=255, fill=1) #center filled
draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
image.show()
#disp.display()   
time.sleep(.01) 
