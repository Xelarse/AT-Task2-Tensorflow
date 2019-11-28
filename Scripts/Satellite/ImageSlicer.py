import numpy as np
import cv2
from pathlib import Path
import os
import math
import time

SLICE_X = 300
SLICE_Y = 300
START_FILEPATH = "D:\Alex\Documents\ProjectsAndWork\PyCharm\AT-Task2-Tensorflow\Dataset\Satellite\RawImages"
END_FILEPATH = "D:\Alex\Documents\ProjectsAndWork\PyCharm\AT-Task2-Tensorflow\Dataset\Satellite\ChoppedImages"


# START_FILEPATH = input("Please input path pictures are found in: ")
# END_FILEPATH = input("Please input path to put split images: ")
# SLICE_X = input("Please input the width of each split image in pixels: ")
# SLICE_Y = input("Please input the height of each split image in pixels: ")

SLICE_X = int(SLICE_X)
SLICE_Y = int(SLICE_Y)

def splice_image(img):
    img_width, img_height = img.shape[:2]
    x_tiles = math.floor(img_width / SLICE_X)
    y_tiles = math.floor(img_height / SLICE_Y)
    image_start_timestamp = f"{int(time.time())}"
    for y in range(y_tiles):
        for x in range(x_tiles):
            current_x_step = x * SLICE_X
            current_y_step = y * SLICE_Y
            sliced_img = img[current_y_step:current_y_step+SLICE_Y, current_x_step:current_x_step+SLICE_X]
            file_name = f"\\{image_start_timestamp}--{x},{y}.png"
            cv2.imwrite(END_FILEPATH + file_name, sliced_img)


for img in os.listdir(START_FILEPATH):
    img_array = cv2.imread(os.path.join(START_FILEPATH, img), cv2.IMREAD_COLOR)
    splice_image(img_array)