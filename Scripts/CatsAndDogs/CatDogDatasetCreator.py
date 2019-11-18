import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random

DATADIR = "D:/Alex/Documents/ProjectsAndWork/PyCharm/AT-Task2-Tensorflow/Dataset/CatsVDogs/train"
CATEGORIES = ["Dogs", "Cats"]
IMG_SIZE = 50

training_data = []


def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)      # When classifying between dog or cat we need an value not a string so use the index of CATEGORIES to relate to the cat and dog
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                normalized_img = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([normalized_img, class_num])       # Add the image and classification for image to the training data dictionary
            except Exception as e:
                pass    # Just in case there is an issue with a specific image skip it so it doesnt break the whole training process


create_training_data()
random.shuffle(training_data)

X = []      # Generally capital X for feature set, in this case its the image
y = []      # Generally lowercase y for labels, in this case its cat or dog

# Split the list of features and labels to their own separate arrays for keras
for features, label in training_data:
    X.append(features)
    y.append(label)

# Inputting X needs to be converted to a numpy array when getting passed into keras
# -1 is a catch all so reshape all indexes to IMG_SIZE x IMG_SIZE. 1 as the last parameter cause its grayscale only 1 layer to the image as opposed to 3 in rgb
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

# Save out the dataset as we dont want to have to rebuild this every time we tweak the CNN
# To load back in later just use X = np.load("CatDogFeatures.npy")
np.save("CatDogFeatures.npy", X)
np.save("CatDogLabels.npy", y)


#### Test example below for seeing how to work with importing data in
# Loop over each category in the path
# for category in CATEGORIES:
#    # Append the category onto the the full filepath
#    path = os.path.join(DATADIR, category)
#
#    # Loop over each image in the directory specified by path
#    for img in os.listdir(path):
#        # We read in the image by taking the previous path and adding this images name to the path, Grayscale as
#        # colour in this case isn't as important for identifying between cat and dog
#        img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
#
#        # Use matplotlib to show the image
#        plt.imshow(img_array, cmap="gray")
#        plt.show()
#
#        # Normalise the size of the img so that all images follow the same convention
#        normalized_img = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
#        plt.imshow(normalized_img, cmap="gray")
#        plt.show()
#        break
#    break
