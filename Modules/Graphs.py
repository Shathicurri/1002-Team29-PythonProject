import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox


def Bar_Graph(output, tv2):
    """"This function plots the bar graph as well as displays it"""

    if len(tv2.get_children()) < 1:
        messagebox.showerror("No Data!", "No data available to display")
        return None
    else:
        graph_data = pd.DataFrame(np.array(output))
        graph_data.columns = ['Prediction', 'Protocol', 'Dst Port', 'Timestamp']

        exclude = ['Benign']
        newdf = graph_data[~graph_data.Prediction.isin(exclude)]

        # Counting each row and converting to list
        x_axis = newdf['Dst Port'].value_counts().keys().tolist()  # Values for X-Axis
        y_axsis = newdf['Dst Port'].value_counts().tolist()  # Values fro Y-Axis

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title('Number of Attack on Ports', fontsize=22)  # Title of Chart
        ax.set_ylabel('# of Attack')  # Y-Axis label for Bar graph
        ax.set_xlabel('Destination Ports')  # X-Axis label for Bar graph
        ax.bar(x_axis[:5], y_axsis[:5])
        plt.show()


def Pie_chart(output, tv2):
    """This function plots the pie chart as well as displays it"""

    if len(tv2.get_children()) < 1:
        messagebox.showerror("No Data!", "No data available to display")
        return None
    else:
        graph_data = pd.DataFrame(np.array(output))
        graph_data.columns = ['Prediction', 'Protocol', 'Dst Port', 'Timestamp']

        # Excluded Benign from the attacks
        exclude = ['Benign']
        newdf = graph_data[~graph_data.Prediction.isin(exclude)]

        # Counting each row and converting to list
        attack = newdf['Prediction'].value_counts().keys().tolist()
        count = newdf['Prediction'].value_counts().tolist()

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title('Number of Each Cyber Attack', fontsize=22)  # Title of Chart

        # Plot of Pie Chart (Consist of All attacks)
        ax.pie(count, autopct=lambda p: '({:.0f})'.format(p * sum(count) / 100), startangle=90)

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.legend(labels=attack)  # Legend for Pie and Donut Chart
        plt.show()


def Donut_chart(output, tv2):
    """This function plots the donut chart as well as displays it"""

    if len(tv2.get_children()) < 1:
        messagebox.showerror("No Data!", "No data available to display")
        return None
    else:
        graph_data = pd.DataFrame(np.array(output))
        graph_data.columns = ['Prediction', 'Protocol', 'Dst Port', 'Timestamp']

        # Excluded Benign from the attacks
        exclude = ['Benign']
        newdf = graph_data[~graph_data.Prediction.isin(exclude)]

        # Counting each row and converting to list
        attack = newdf['Prediction'].value_counts().keys().tolist()
        count = newdf['Prediction'].value_counts().tolist()

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title('Number of Each Cyber Attack', fontsize=22)  # Title of Chart

        # Plot of Donut Chart (Consist of Top 5 attacks)
        ax.pie(count[:5], autopct=lambda p: '({:.0f})'.format(p * sum(count[:5]) / 100), startangle=90)

        # Making Pie Chart into a Donut
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        plt.legend(labels=attack[:5])  # Legend for Pie and Donut Chart
        plt.show()
