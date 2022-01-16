from enum import Enum
from statistics import mode
import time
from turtle import width
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class image_interface:


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
            self.disp - None
        except Exception:

            exit(0)


        self.image = Image.new('1', (self,width, self.height))

        if self.mode == self.modes.TEST:
            print("a")


    def update_image(self, image:Image):
        self.image = image
        

    def get_image(self):
        return self.image


import tkinter
global i
i = 0
root = tkinter.Tk()
label = tkinter.Label(root)
label.pack()
img = None
tkimg = [None]  # This, or something like it, is necessary because if you do not keep a reference to PhotoImage instances, they get garbage collected.





delay = 50   # in milliseconds
def loopCapture():
    global i
    print("capturing")
    width = 128#disp.width
    height = 64#disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    i += 1
    draw.polygon([(20, 20), (30, 2), (40, 20+i)], outline=255, fill=1)  #Up filled


    tkimg[0] = ImageTk.PhotoImage(image)
    label.config(image=tkimg[0])
    root.update_idletasks()
    root.after(delay, loopCapture)

loopCapture()
root.mainloop()