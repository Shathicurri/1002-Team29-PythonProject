import pandas as pd
import numpy as np
from numpy import argmax
from tensorflow.keras.models import load_model


def Prediction(label_file, tv2):
    """"This function loads the model from Tensorflow and and does the prediction"""
    """Which is later displayed"""

    atks = {
        0: 'Benign',
        1: 'Bot',
        2: 'BruteForce - Web',
        3: 'BruteForce - XSS',
        4: 'DDOS attack - HOIC',
        5: 'DoS attacks - GoldenEye',
        6: 'DoS attacks - Hulk',
        7: 'DoS attacks - SlowHTTPTest',
        8: 'DoS attacks - Slowloris',
        9: 'FTP - BruteForce',
        10: 'Infilteration',
        11: 'SQL Injection',
        12: 'SSH - Bruteforce'
    }

    df = pd.read_csv(label_file["text"])
    data = pd.DataFrame(df)
    timestamp = data.pop('Timestamp')

    # Run the current data through the model to get the predictions
    model = load_model("model/training_3.h5")
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    predictions = model.predict(data.values)

    output = []

    # Combines the dataset to display
    for p1, p2, p3, t in zip(predictions, df['Protocol'].values, df['Dst Port'].values, timestamp):
        small_output = []
        small_output.append(atks[argmax(p1)])
        small_output.append(int(p2))
        small_output.append(int(p3))
        small_output.append(t)
        output.append(small_output)

    combination1 = pd.DataFrame(np.array(output))

    # Displays the data
    tv2["column"] = ['Prediction', 'Protocol', 'Dst Port', 'Timestamp']
    tv2["show"] = "headings"
    for column in tv2["columns"]:
        tv2.heading(column, text=column)  # let the column heading = column name

    df_rows = combination1.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        tv2.insert("", "end", values=row)

    return output
