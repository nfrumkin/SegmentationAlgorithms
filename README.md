# Segmentation Algorithms

## Installation Instructions
Python Version = 3.6.6
## Load Modules and Pip install
On SCC:

    module load python3
    pip3 install --user PyMaxFlow

*note*: Must use ssh -X for GUI!!

### Python API Packages
* python-tk
* PIL
* numpy
* pickle
* scipy
* maxflow
* matplotlib
* skimage

## Running Application
### Step 1: Image Annotation

`python3 image_gui.py`

1. Click on foreground
2. Click-and-drag to annotate foreground of image
3. Click on background
4. Click-and-drag to annotate background of image
5. Click "Finish Labelling"
6. Close pop-up

### Step 2: Max Flow Image Segmentor
`python3 max-flow.py`

### Step 3: Otsu Thresholding
`python3 otsu_thresholding.py`

