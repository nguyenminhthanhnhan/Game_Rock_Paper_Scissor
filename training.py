import cv2
import numpy as np
# from keras_squeezenet import SqueezeNet
from keras.applications import MobileNet
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D, Dense
from keras.models import Sequential
import tensorflow as tf
import os

IMG_SAVE_PATH = 'images'

CLASS_MAP = {
    "rock": 0,
    "paper": 1,
    "scissors": 2,
    "nothing": 3
}

NUM_CLASSES = len(CLASS_MAP)


def mapper(val):
    return CLASS_MAP[val]

def get_model():
    base_model = MobileNet(input_shape=(227, 227, 3), include_top=False)
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dropout(0.5),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    return model

# def get_model():
#     model = Sequential([
#         SqueezeNet(input_shape=(227, 227, 3), include_top=False),
#         Dropout(0.5),
#         Convolution2D(NUM_CLASSES, (1, 1), padding='valid'),
#         Activation('relu'),
#         GlobalAveragePooling2D(),
#         Activation('softmax')
#     ])
#     return model


# load images from the directory
dataset = []
for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join(IMG_SAVE_PATH, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        # to make sure no hidden files get in our way
        if item.startswith("."):
            continue
        img = cv2.imread(os.path.join(path, item))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        dataset.append([img, directory])

data, labels = zip(*dataset)
labels = list(map(mapper, labels))


# one hot encode the labels
labels = to_categorical(labels, NUM_CLASSES)

# define the model
model = get_model()
model.compile(
    optimizer=Adam(lr=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# start training
model.fit(np.array(data), np.array(labels), epochs=15)

# save the model for later use
model.save("game-model.h5")