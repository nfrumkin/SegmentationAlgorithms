from skimage.filters import threshold_otsu
import os.path as path
import matplotlib.pyplot as plt
from skimage import io, color
import numpy as np
import time

img = io.imread(path.expanduser('imgs/chicken.jpg'))
start = time.time()
r_t = threshold_otsu(img[:, :, 0])
g_t = threshold_otsu(img[:, :, 1])
b_t = threshold_otsu(img[:, :, 2])
end = time.time()
print("elapsed: ", end-start)

m = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
mask = (img[:, :, 0] < r_t) & (img[:, :, 1] < g_t) & (img[:, :, 2] < b_t)
m[~mask] = 255

plt.imshow(m)
plt.show()