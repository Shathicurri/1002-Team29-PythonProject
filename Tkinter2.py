import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from numpy import argmax
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import normalize
import easygui

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

# initalise the tkinter GUI
root = tk.Tk()

root.geometry("700x700") # set the root dimensions
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0) # makes the root window fixed in size.

tabcontrol = ttk.Notebook(root)
tab1 = ttk.Frame(tabcontrol)
tab2 = ttk.Frame(tabcontrol)
tab3 = ttk.Frame(tabcontrol)
tabcontrol.add(tab1, text='Tab 1')
tabcontrol.add(tab2, text='Tab 2')
tabcontrol.add(tab3, text='Tab 3')
tabcontrol.pack(expand=1, fill="both")

# Frame for TreeView
frame1 = tk.LabelFrame(tab1, text="Excel Data")
frame1.place(height=250, width=500)

frame2 = tk.LabelFrame(tab2, text="Graph")
frame2.place(height=250, width=500)

frame3 = tk.LabelFrame(tab3, text="Prediction")
frame3.place(height=500, width=500)

# Frame for open file dialog
file_frame = tk.LabelFrame(tab1, text="Open File")
file_frame.place(height=300, width=400, rely=0.4, relx=0)

# Buttons
button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
button1.place(rely=0.30, relx=0.50)

button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
button2.place(rely=0.30, relx=0.30)

buttonExport = tk.Button(file_frame, text="Export File", command=lambda: Export_excel_data())
buttonExport.place(rely=0.30, relx=0.80)

buttonGet = tk.Button(file_frame, text="Search", command=lambda: Search())
buttonGet.place(rely=0.65, relx=0.65)

buttonBar = tk.Button(frame2, text="Bar Graph", command=lambda: Bar_Graph())
buttonBar.place(rely=0.30, relx=0.80)

# Values to enter for Search function
# Entry
entry1 = tk.Entry(file_frame)
entry1.place(rely=0.70, relx=0.30)
entry2 = tk.Entry(file_frame)
entry2.place(rely=0.90, relx=0.30)

# The file/file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)

## Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

tv2 = ttk.Treeview(frame3)
tv2.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame3, orient="vertical", command=tv2.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame3, orient="horizontal", command=tv2.xview) # command means update the xaxis view of the widget
tv2.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

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

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

    # fig, ax = plt.subplots()
    # ax.bar(df['Label'].value_counts().keys().tolist(), df['Label'].value_counts().tolist())
    Prediction()

def Export_excel_data():
    if len(tv1.get_children()) < 1:
        messagebox.showerror("No Data!", "No data available to export")
        return None
    savdia = filedialog.asksaveasfilename(initialdir="/",title="Save File",defaultextension=".csv" ,filetypes=(("CSV File","*.csv"), ("All Files","*")))
    with open(savdia,mode='w') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',')
        for row_id in tv1.get_children():
            row = tv1.item(row_id)["values"]
            exp_writer.writerow(row)

    messagebox.showinfo("Data Exported","Your data has been exported successfully.")

def clear_data():
    tv1.delete(*tv1.get_children())
    return None

def Search():
    clear_data()

    df = pd.read_csv(label_file["text"])

    data1 = entry1.get()
    data2 = entry2.get()

    if data1 != "":
        df_filter = df.loc[df['Dst Port'] == int(data1)]
        df_rows = df_filter.to_numpy().tolist()  # turns the dataframe into a list of lists
        for row in df_rows:
            tv1.insert("", "end",
                        values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    elif data2 != "":
        df_filter = df.loc[df['Protocol'] == int(data2)]
        df_rows = df_filter.to_numpy().tolist()  # turns the dataframe into a list of lists
        for row in df_rows:
            tv1.insert("", "end",
                       values=row)
    else:
        # easygui.msgbox("Invalid Input", title="Wrong Input")
        tk.messagebox.showerror(title="Invalid", message="Invalid Input")

def Bar_Graph():
    plt.show()

def Prediction():

    atks = {
        0:'Benign',
        1:'Bot',
        2:'BruteForce - Web',
        3:'BruteForce - XSS',
        4:'DDOS attack - HOIC',
        5:'DoS attacks - GoldenEye',
        6:'DoS attacks - Hulk',
        7:'DoS attacks - SlowHTTPTest',
        8:'DoS attacks - Slowloris',
        9:'FTP - BruteForce',
        10:'Infilteration',
        11:'SQL Injection',
        12:'SSH - Bruteforce'
    }

    output = []

    df = pd.read_csv(label_file["text"])
    data = pd.DataFrame(df)
    timestamp = data.pop('Timestamp')

    model = load_model("model/training_2.h5")
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    predictions = model.predict(data.values)


    for p1, p2, p3, t in zip(predictions, df['Protocol'].values, df['Dst Port'].values, timestamp):
        small_output = []
        small_output.append(atks[argmax(p1)])
        small_output.append(int(p2))
        small_output.append(int(p3))
        small_output.append(t)
        output.append(small_output)

    for i in range(10):
        print(output[i])
    # combination = zip(predictions, df['Dst Port'], df['Protocol'], timestamp)
    combination1 = pd.DataFrame(np.array(output))
    print(combination1)

    tv2["column"] = ['Prediction', 'Protocol', 'Dst Port',  'Timestamp']
    tv2["show"] = "headings"
    for column in tv2["columns"]:
        tv2.heading(column, text=column)  # let the column heading = column name

    df_rows = combination1.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        tv2.insert("", "end", values=row)


root.mainloop()