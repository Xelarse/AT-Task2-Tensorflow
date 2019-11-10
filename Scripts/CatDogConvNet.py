import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

# Load in data from previously made dataset
X = np.load("CatDogFeatures.npy")
y = np.load("CatDogLabels.npy")

# Time to normalise the data! since pixel data is from 0 - 255 divide by 255
X = X/255.0

model = Sequential()

#### This is the first sort of layer of neurons in the network, these will then feed into another layer then be processed to output

# Add the first Conv layer, with a 3x3 window and the shape being based of X but skipping the first element as previously it was set to -1
model.add(Conv2D(64, (3, 3), input_shape=X.shape[1:]))

# Next is the activation layer using Rectified linear
model.add(Activation("relu"))

# Next is the pooling layer
model.add(MaxPooling2D(pool_size=(2, 2)))

#### Second layer taking the previous neurons output as input

model.add(Conv2D(64, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

#### Finally before output flatten data to 1D and Dense it

model.add(Flatten())
model.add(Dense(64))


#### And the output layer

model.add(Dense(1))
model.add(Activation("sigmoid"))

#### Compile and test fitness
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(X, y, batch_size=32, epochs=10, validation_split=0.1)
