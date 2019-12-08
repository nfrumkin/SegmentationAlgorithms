from image_gui import *
import PIL

img_path = "imgs/cow.jpg"

img = PIL.Image.open(img_path)
grayscale_img = img.convert('LA')

for i in range(grayscale_img.size[0]):
    for j in range(grayscale_img.size[1]):
        print(grayscale_img.getpixel((i,j))[0])
# start_gui(img_path)