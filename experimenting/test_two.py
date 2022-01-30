from string import hexdigits
import tkinter as tk
from threading import *
from turtle import heading, width
from PIL import ImageTk, Image, ImageDraw
import time

width = 128
height = 64

drawn_image = Image.new('1', (width, height))
img = ImageTk.PhotoImage(drawn_image)

def threading():
    # Call work function
    t1=Thread(target=work)
    t1.start()
  
# work function
def work():
    global drawn_image, width, height, img

    print("sleep time start")
  
    for i in range(100):
        draw = ImageDraw.Draw(drawn_image)
        draw.rectangle((0,0,64,128), outline=0, fill=0)
        draw.polygon([(20, 20), (30, 2), (40, 20+i)], outline=255, fill=1)
        img = ImageTk.PhotoImage(drawn_image)

        print(i)
        time.sleep(0.1)
  
    print("sleep time stop")

root = tk.Tk()

panel = tk.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

def callback():
    img2 = ImageTk.PhotoImage(drawn_image)
    panel.configure(image=img2)
    panel.image = img2

threading()

root.bind("<Return>", callback)
root.after(10, callback)
root.mainloop()
