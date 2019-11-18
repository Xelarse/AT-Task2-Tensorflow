import numpy as np
import os
import cv2
import random
from pathlib import Path

DATADIR = "D:\\Alex\\Documents\\ProjectsAndWork\\PyCharm\\AT-Task2-Tensorflow\\Dataset\\Satellite\\Sorted"
EXPORTDIR = "D:\\Alex\\Documents\\ProjectsAndWork\\PyCharm\\AT-Task2-Tensorflow\\Dataset\\Satellite\\ExportedTrainingData"
CATEGORIES = ["City Building", "Dense Forest", "Grass", "Road", "Sand", "Sparse Forest", "Village Building", "Water"]
IMG_SIZE = 50

training_data = []

def create_training_data():
    for cat in CATEGORIES:
        path = os.path.join(DATADIR, cat)
        class_num = CATEGORIES.index(cat)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_COLOR)
                training_data.append([img_array, class_num])
                print(f"Processing: {os.path.join(path, img)} in Category: {cat}")
            except Exception as e:
                pass


create_training_data()
random.shuffle(training_data)

X = []
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)

# X needs to be converted to np array for Keras to use, ensure IMG_SIZE matches img res
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

features_name = "SatelliteFeatures.npy"
labels_name = "SatelliteLabels.npy"
features_path = os.path.join(EXPORTDIR, features_name)
labels_path = os.path.join(EXPORTDIR, labels_name)

if Path(features_path).is_file():
    os.remove(features_path)

if Path(labels_path).is_file():
    os.remove(labels_path)

np.save(features_path, X)
np.save(labels_path, y)
