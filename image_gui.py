# GUI library
import tkinter as tk
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import numpy as np

xCoords = []
yCoords = []
annotation_values = []

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'green'

    def __init__(self, paint_utils_frame):
        self.root = paint_utils_frame

        self.fgd_button = Button(self.root, text='foreground label', command=self.label_fgd)
        self.fgd_button.grid(row=0, column=0)

        self.bgd_button = Button(self.root, text='background label', command=self.label_bgd)
        self.bgd_button.grid(row=0, column=1)


        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        path = "imgs/cow.jpg"
        img = ImageTk.PhotoImage(Image.open(path))
        imgHeight = img.height()
        imgWidth = img.width()
        self.c = Canvas(self.root, bg='white', width=imgWidth, height=imgHeight)
        self.c.create_image(self.root.winfo_x(),self.root.winfo_y(), image=img, anchor=tk.NW)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        # 0 is foreground, 1 is background
        self.ann_mode = 0
        self.active_button = self.fgd_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)
    
    def label_fgd(self):
        self.color = "green"
        self.ann_mode = 0
        self.activate_button(self.fgd_button)

    def label_bgd(self):
        self.color = "red"
        self.ann_mode = 1
        self.activate_button(self.bgd_button)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        # self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=self.color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

        # save label coordinates
        xCoords.append(event.x)
        yCoords.append(event.y)
        annotation_values.append(self.ann_mode)
        print('{}, {}, {}'.format(event.x, event.y, self.ann_mode))

    def reset(self, event):
        self.old_x, self.old_y = None, None


def createImage():
    print("width: ", imgWidth, "height: ", imgHeight)
    imgArray = np.zeros([imgWidth,imgHeight])
    for i in range(0,len(xCoords)):
        imgArray[xCoords[i], yCoords[i]] = 1
    
    #todo: PIL.Image.fromarray()
    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
    

def endLabel():
    print("end labelling")
    # imgWidth = panel2.winfo_reqwidth()
    # imgHeight = panel2.winfo_reqheight()
    createImage()

def start_gui(path):
    root = tk.Tk()
    # splice gui into top and bottom panels
    top = tk.Frame(root)
    paint_utils_frame = tk.Frame(root)
    middle = tk.Frame(root)
    bottom = tk.Frame(root)
    top.pack(side="top")
    paint_utils_frame.pack(side="top")
    middle.pack(side="top")
    bottom.pack(side="bottom", fill="both", expand=True)

    title = tk.Label(root, text="Annotate foreground and background. Click buttons to begin, click \"Finish labelling\" when done")
    title.pack(in_=top, side="left")

    # end label button
    endButton = tk.Button(middle, text="finish labelling", command=endLabel)
    endButton.pack(in_=middle, side="left")

    Paint(paint_utils_frame)

    root.mainloop()

if __name__ == "__main__":
    img_path = "imgs/cow.jpg"
    start_gui(img_path)