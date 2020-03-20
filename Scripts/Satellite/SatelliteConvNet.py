import tensorflow as tf
import numpy as np
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import time
import os


export_model = True
dense_layers = [1]
dense_sizes = [256, 512]
layer_sizes = [64, 128, 256]
conv_layers = [2]
kern_sizes = [7]
model_runs = [200, 300, 500, 1000]

pathToScript = os.getcwd()

# cd to log directory
# !tensorboard --logdir ./

# Load in data from previously made dataset
X = np.load("D:\\Alex\\Documents\\ProjectsAndWork\\ThirdYear\\AT-Task2-Tensorflow\\Dataset\\Satellite\\ExportedTrainingData\\SatelliteFeatures.npy")
y = np.load("D:\\Alex\\Documents\\ProjectsAndWork\\ThirdYear\\AT-Task2-Tensorflow\\Dataset\\Satellite\\ExportedTrainingData\\SatelliteLabels.npy")

# Time to normalise the data! since pixel data is from 0 - 255 divide by 255
#X = X/255.0
y = keras.utils.to_categorical(y, 8)
# Make multiple models with each of the variations above

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            for dense_size in dense_sizes:
                for kern_size in kern_sizes:
                    for epoc in model_runs:
                        NAME = f"Satellite-{conv_layer}-conv-{layer_size}-nodes-{dense_layer}-dense-{dense_size}-dense_size-{kern_size}-kernel_size-{epoc}-Epochs-{int(time.time())}"
                        tensorboard = TensorBoard(log_dir=os.path.join(pathToScript, "logs\\{}".format(NAME)))
                        print(NAME)

                        model = Sequential()

                        model.add(Conv2D(layer_size, (kern_size, kern_size), input_shape=X.shape[1:]))
                        model.add(Activation("relu"))
                        model.add(MaxPooling2D(pool_size=(2, 2)))
                        model.add(Dropout(0.25))

                        # First conv layer must have input shape but every one after is the same
                        for l in range((conv_layer-1)):
                            model.add(Conv2D(layer_size, (kern_size, kern_size)))
                            model.add(Activation("relu"))
                            model.add(MaxPooling2D(pool_size=(2, 2)))
                            model.add(Dropout(0.25))

                        model.add(Flatten())
                        for l in range(dense_layer):
                            model.add(Dense(dense_size))
                            model.add(Activation("relu"))
                            model.add(Dropout(0.5))

                        model.add(Dense(8))
                        model.add(Activation("softmax"))

                        #### Compile and fit
                        model.compile(loss="categorical_crossentropy", optimizer="adadelta", metrics=["accuracy"])
                        model.fit(X, y, batch_size=32, epochs=epoc, validation_split=0.3, callbacks=[tensorboard], shuffle=True)

                        if(export_model):
                            model.save(f"models/Satellite-{conv_layer}-conv-{layer_size}-nodes-{dense_layer}-dense-{dense_size}-dense_size-{kern_size}-kernel_size-{epoc}-Epochs.h5")
