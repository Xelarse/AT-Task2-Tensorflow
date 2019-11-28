import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import cv2
import math
import matplotlib.pyplot as plt
import time
import os
import json

CATEGORIES = ["City Building", "Dense Forest", "Grass", "Road", "Sand", "Sparse Forest", "Village Building", "Water"]
IMG_SIZE = 50


# First take an image from the specified file path and a model to use for prediction

img_path = "D:\\Alex\\Documents\\ProjectsAndWork\\PyCharm\\AT-Task2-Tensorflow\\Dataset\\Satellite\\RawImages\\1574957771.png" # input("Please enter file path to Img: ")
model_path = "D:\\Alex\\Documents\\ProjectsAndWork\\PyCharm\\AT-Task2-Tensorflow\\Scripts\\Satellite\\models\\Satellite-2-conv-128-nodes-1-dense-20-epochs.h5" #input("Please enter file path to Model: ")

full_img = cv2.imread(img_path, cv2.IMREAD_COLOR)
model = tf.keras.models.load_model(model_path)

# Split the image up into 50 x 50 chunks, as they're being split classify them and add to array

img_width, img_height = full_img.shape[:2]
x_tiles = math.floor(img_width / IMG_SIZE)
y_tiles = math.floor(img_height / IMG_SIZE)
json_array = []
for y in range(y_tiles):
    for x in range(x_tiles):
        current_x_step = x * IMG_SIZE
        current_y_step = y * IMG_SIZE
        sliced_img = full_img[current_y_step:current_y_step + IMG_SIZE, current_x_step:current_x_step + IMG_SIZE]
        resized_img = cv2.resize(sliced_img, (IMG_SIZE, IMG_SIZE))
        reshaped_img = resized_img.reshape(-1, IMG_SIZE, IMG_SIZE, 3)
        prediction = model.predict(reshaped_img)
        predicted_index = -1
        print(f"X: {x}, Y: {y} --")
        for index in range(len(prediction[0])):
            print(CATEGORIES[index] + ": ", prediction[0][index])
            if prediction[0][index] > 0:
                if predicted_index == -1:
                    predicted_index = index
                elif prediction[0][index] > prediction[0][predicted_index]:
                    predicted_index = index
        predict_text = f"{CATEGORIES[predicted_index]}" if predicted_index != -1 else "NA"
        obj = {}
        obj["XCord"] = x
        obj["YCord"] = y
        obj["Type"] = predict_text
        json_array.append(obj)

# Output json based on the array
print(json_array)
output_name = "JSONS/" + os.path.basename(img_path) + "-jsonFile.txt"
json.dump(json_array, open(output_name, "w"))
