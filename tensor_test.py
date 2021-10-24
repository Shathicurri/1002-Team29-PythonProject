import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Read the file to get the values for the labels
data = pd.read_csv('Book3.csv')
data = pd.DataFrame(data)
label = data.pop('Label')
title = label.pop(0)

# Read the file to get the dataset for the samples
data2 = pd.read_csv('Book4.csv')

# Converts the lists to a tensor object
train_labels = tf.convert_to_tensor(label)
train_samples = tf.convert_to_tensor(data2)

# Create the model using sequential the identify the layers it should go through
model = keras.Sequential([
    # 1st layer mostly to specify the input shape
    Dense(units=18, input_shape=(722, 78), activation='relu'),
    Dense(units=32, activation='relu'),
    # 3rd layer is to split the data into either 1 of the 13 units
    Dense(units=13, activation='softmax')
])

# This will compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# This will train the model with the given datasets
model.fit(train_samples, train_labels, batch_size=75, epochs=600, verbose=1)

# This will save the model that was used to train
model.save("model/training_3.h5")
