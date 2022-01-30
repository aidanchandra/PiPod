
from doctest import UnexpectedException
from enum import Enum
from statistics import mode
import threading
import time
from turtle import width
from PIL import Image,ImageTk,ImageDraw, ImageFont
import tkinter


class image_interface:

    SCREEN_PERIOD = 1/60
    class modes(Enum):
        TEST=1
        LIVE=0
    
    """
        Master interace class to switch between simulating an image output
    """

    def __init__(self) -> None:

        self.width = 128
        self.height = 64

        #Libraries available on every OS - regardless of testing

        try:
            import RPi.GPIO as GPIO
            import Adafruit_GPIO.SPI as SPI
            import Adafruit_SSD1306

            self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
            self.disp.begin()
            self.disp.clear()
            self.disp.display()

            #self.disp.image(image)
            #self.disp.display()  

            self.mode = self.modes.LIVE
        except ImportError:
            self.mode = self.modes.TEST
            self.disp = None
        except Exception:
            print("There must be an error in establishing connection")
            exit(0)


        self.image = Image.new('1', (self.width, self.height))

        self.update_screen()

    def update_image(self, image:Image):
        self.image = image
        self.update_screen()

    def get_image(self):
        return self.image

    def update_screen(self):
        #threading.Timer(self.SCREEN_PERIOD,self.update_screen).start()
        if self.mode == self.modes.LIVE:
            self.disp.image(self.image)
            self.disp.display()  
        else:
            self.image.save("tmp.png","PNG")

if __name__ == "__main__":
    display_interface = image_interface()
    image = display_interface.get_image()
    draw = ImageDraw.Draw(image)

    for i in range(0,100):
        draw.rectangle((0,0,64,128), outline=0, fill=0)
        draw.polygon([(20, 20), (30, 2+i), (40, 20+i)], outline=255, fill=1)  #Up filled
        display_interface.update_image(image)
        time.sleep(1)