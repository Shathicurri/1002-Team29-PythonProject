import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy

data = pd.read_csv('Book3.csv')
data = pd.DataFrame(data)

data2 = pd.read_csv('Book4.csv')
# data2 = [123,235,456,879,54,21,54,65,87]

label = data.pop('Label')
title = label.pop(0)
# label = ['as', 'df','fg', 'hj','hty','ert','yuki','bnm','iuop']
# label = [0,1,4,1,3,1,0,0,2]
# print(data.columns)
# print(label.shape)
print(data2.shape)

train_samples = data2
train_labels = label
print(train_labels)

# count = 0
# for i in train_samples:
#     if type(i) != string:
#         count += 1
#     else:
#         print(i)

train_labels = tf.convert_to_tensor(train_labels)
train_samples = tf.convert_to_tensor(train_samples)
# tf.keras.preprocessing.sequence.pad_sequences(train_samples)

print(train_samples.dtype)

# train_labels, train_samples = shuffle(train_labels, train_samples)

print(train_samples)

# scalar = MinMaxScaler(feature_range=(0,1))
# scaled_train_samples = scalar.fit_transform(train_samples.reshape(-1,1))

model = keras.Sequential([
    Dense(units=18, input_shape=(722, 78), activation='relu'),
    Dense(units=32, activation='relu'),
    Dense(units=13, activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(train_samples, train_labels, batch_size=75, epochs=600, verbose=1)

model.save("model/training_3.h5")
