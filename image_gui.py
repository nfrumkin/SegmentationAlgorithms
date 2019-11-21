# GUI library
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

root = tk.Tk()
# splice gui into top and bottom panels
top = tk.Frame(root)
middle = tk.Frame(root)
bottom = tk.Frame(root)
top.pack(side="top")
middle.pack(side="top")
bottom.pack(side="bottom", fill="both", expand=True)

xCoords = []
yCoords = []

def saveCoordinates(x,y):
    xCoords.append(x)
    yCoords.append(y)

def createImage():
    print("width: ", imgWidth, "height: ", imgHeight)
    imgArray = np.zeros([imgWidth,imgHeight])
    for i in range(0,len(xCoords)):
        imgArray[xCoords[i], yCoords[i]] = 1
    
def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

    saveCoordinates(x,y)


def endLabel():
    print("end labelling")
    # imgWidth = panel2.winfo_reqwidth()
    # imgHeight = panel2.winfo_reqheight()
    createImage()

title = tk.Label(root, text="Manual Image Annotation: Outline foreground of image. Annotate using click-and-drag.")
title.pack(in_=top, side="left")

# end label button
endButton = tk.Button(root, text="finish labelling", command=endLabel)
endButton.pack(in_=middle, side="left")

# bottom panel to display image
path = "imgs/cow.jpg"
img = ImageTk.PhotoImage(Image.open(path))
imgHeight = img.height()
imgWidth = img.width()
panel2 = tk.Label(root, image = img)
panel2.pack(in_=bottom, side = "left", fill = "both", expand = "yes")

# click-and-drage mouse event
root.bind("<B1-Motion>", motion)
root.mainloop()