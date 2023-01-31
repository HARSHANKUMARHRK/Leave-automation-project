import tensorflow as tf
from tensorflow import keras

# load MNIST dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data("train.gz")

# preprocess data
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# build model
model = keras.Sequential([
    keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# compile model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# train model
model.fit(x_train, y_train, epochs=5)

# evaluate model
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print('\nTest accuracy:', test_acc)

import numpy as np

# preprocess custom input data
custom_input = np.array([["hello"]]) # replace ... with your data
custom_input = custom_input.reshape(custom_input.shape[0], 28, 28, 1)
custom_input = custom_input.astype('float32') / 255

# make predictions on custom input
predictions = model.predict(custom_input)

# convert predictions to class labels
predicted_classes = np.argmax(predictions, axis=1)

