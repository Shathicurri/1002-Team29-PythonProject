import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib as mlp
import matplotlib.pyplot as plt
import os

import pandas as pd

# initalise the tkinter GUI
root = tk.Tk()

root.geometry("500x500") # set the root dimensions
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0) # makes the root window fixed in size.

# Frame for TreeView
frame1 = tk.LabelFrame(root, text="Excel Data")
frame1.place(height=250, width=500)

# Frame for open file dialog
file_frame = tk.LabelFrame(root, text="Open File")
file_frame.place(height=100, width=400, rely=0.65, relx=0)

# Buttons
button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.30)

# buttonExport = tk.Button(file_frame, text="Export File", command=lambda: Export_excel_data())
# buttonExport.place(rely=0.65, relx=0.80)

#Stop the frame from propagating the widget to be shrink or fit
frame1.pack_propagate(False)

# The file/file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)


def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("Csv Files","*.csv"),("All Files", "*.*")))
    label_file["text"] = filename
    return None


def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    # Exclude out 'Benign' into the charts
    exclude = ['Benign']
    newdf = df[~df.Label.isin(exclude)]

    fig, ax = plt.subplots(figsize=(8,5))
    count = newdf['Label'].value_counts().tolist() # Declaring Count of Cyber attacks to LIST
    attack = newdf['Label'].value_counts().keys().tolist() # Declaring Attack of Cyber attacks to LIST

    # Plot of Pie Chart and Donut Chart
    ax.pie(count,labels=attack,autopct=lambda p : '({:.0f})'.format(p * sum(count)/100),startangle = 90)

    # Making Pie Chart into a Donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Plot of Bar graph
    # ax.bar(attack,count)

    ax.set_title('Number of Each Cyber Attack' , fontsize = 22)
    # Y-Axis label for Bar graph
    # ax.set_ylabel('# of Attack')

    # X-Axis label for Bar graph
    # ax.set_xlabel('Type of Cyber Attack')

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')

    plt.legend() # Legend for Pie and Donut Chart
    plt.show()

root.mainloop()