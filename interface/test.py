from doctest import UnexpectedException
from enum import Enum
from statistics import mode
import time
from turtle import width
from PIL import Image,ImageTk,ImageDraw, ImageFont
import tkinter


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
            self.disp = None
        except Exception:
            print("There must be an error in establishing connection")
            exit(0)


        self.image = Image.new('1', (self.width, self.height))

        if self.mode == self.modes.TEST:
            #Start a threat with the display updating

            self.root = tkinter.Tk()
            self.label = tkinter.Label(self.root)
            self.label.pack()
            self.tkimg = [None]  
            delay = 50 
            def loopCapture():

                
                draw = ImageDraw.Draw(self.image)
                draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
                draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                

                self.tkimg[0] = ImageTk.PhotoImage(self.image)
                self.label.config(image=self.tkimg[0])
                self.root.update_idletasks()
                self.root.after(delay, loopCapture)
            loopCapture()
            self.root.mainloop()
            


    def update_image(self, image:Image):
        self.tkimg[1] = ImageTk.PhotoImage(image)

        self.label.config(image=self.tkimg[1])

        if self.mode == self.modes.LIVE:
            self.update_screen()

    def update_screen(self):
        if self.mode != self.modes.LIVE:
            raise UnexpectedException("This method should only ever be called in modes.LIVE")
        else:
            print("Have yet to test :)")
            self.disp.image(self.image)
            self.disp.display() 
        

    def get_image(self):
        return self.image


# global i
# i = 0
# root = tkinter.Tk()
# label = tkinter.Label(root)
# label.pack()
# img = None
# tkimg = [None]  # This, or something like it, is necessary because if you do not keep a reference to PhotoImage instances, they get garbage collected.
# delay = 50   # in milliseconds
# def loopCapture():
#     global i
#     print("capturing")
#     width = 128#disp.width
#     height = 64#disp.height
#     image = Image.new('1', (width, height))

#     # Get drawing object to draw on image.
#     draw = ImageDraw.Draw(image)

#     # Draw a black filled box to clear the image.
#     draw.rectangle((0,0,width,height), outline=0, fill=0)

#     i += 1
#     draw.polygon([(20, 20), (30, 2), (40, 20+i)], outline=255, fill=1)  #Up filled


#     tkimg[0] = ImageTk.PhotoImage(image)
#     label.config(image=tkimg[0])
#     root.update_idletasks()
#     root.after(delay, loopCapture)
# loopCapture()
# root.mainloop()

if __name__ == "__main__":

    image = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(image)

    for i in range(0,100):
        draw.rectangle((0,0,64,128), outline=0, fill=0)
        draw.polygon([(20, 20), (30, 2), (40, 20+i)], outline=255, fill=1)  #Up filled
        image.save("tmp.png","PNG")
        time.sleep(1)
