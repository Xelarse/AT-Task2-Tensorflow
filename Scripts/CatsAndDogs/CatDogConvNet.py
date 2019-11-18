import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import time
import os


export_model = True
dense_layers = [0]
layer_sizes = [64]
conv_layers = [3]

pathToScript = os.getcwd()

# Load in data from previously made dataset
X = np.load("CatDogFeatures.npy")
y = np.load("CatDogLabels.npy")

# Time to normalise the data! since pixel data is from 0 - 255 divide by 255
X = X/255.0

# Make multiple models with each of the variations above

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            NAME = f"CatAndDog-{conv_layer}-conv-{layer_size}-nodes-{dense_layer}-dense-{int(time.time())}"
            tensorboard = TensorBoard(log_dir=os.path.join(pathToScript, "logs\\{}".format(NAME)))
            print(NAME)

            model = Sequential()

            model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:]))
            model.add(Activation("relu"))
            model.add(MaxPooling2D(pool_size=(2, 2)))

            # First conv layer must have input shape but every one after is the same
            for l in range(conv_layer-1):
                model.add(Conv2D(layer_size, (3, 3)))
                model.add(Activation("relu"))
                model.add(MaxPooling2D(pool_size=(2, 2)))

            model.add(Flatten())
            for l in range(dense_layer):
                model.add(Dense(layer_size))
                model.add(Activation("relu"))
                model.add(Dropout(0.2))

            model.add(Dense(1))
            model.add(Activation("sigmoid"))

            #### Compile and fit
            model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
            model.fit(X, y, batch_size=32, epochs=10, validation_split=0.1, callbacks=[tensorboard])

            if(export_model):
                model.save(f"models/CatAndDog-{conv_layer}-conv-{layer_size}-nodes-{dense_layer}-dense.h5")


