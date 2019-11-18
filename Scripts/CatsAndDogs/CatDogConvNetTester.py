import cv2
import tensorflow as tf

CATEGORIES = ["Dog", "Cat"]

def prepare(filepath):
    IMG_SIZE = 50
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    resized_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return resized_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

print("\n\n\n")
model = tf.keras.models.load_model(input("Please define model filepath: "))

while(True):
    # When predicting you ALWAYS gotta do a list, even if its only one thing
    print("\n\n\n")
    prediction = model.predict([prepare(input("Please define test img filepath: "))])

    print(f"The model predicted: {CATEGORIES[int(prediction[0][0])]}")
