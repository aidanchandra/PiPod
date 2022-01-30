from turtle import goto
from PIL import Image,ImageTk,ImageDraw
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
    width = 128#disp.width
    height = 64#disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    i += 1
    draw.polygon([(20, 20), (30, 2), (40, 20+(i%64))], outline=255, fill=1)  #Up filled


    tkimg[0] = ImageTk.PhotoImage(image)
    label.config(image=tkimg[0])
    root.update_idletasks()
    root.after(delay, loopCapture)

loopCapture()
root.mainloop()