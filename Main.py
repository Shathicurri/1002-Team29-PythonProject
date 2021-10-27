import csv
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import numpy as np
from numpy import argmax
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# initalise the tkinter GUI
root = tk.Tk()

root.title("Digital Crime Analyzer")
root.geometry("700x700") # set the root dimensions
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0) # makes the root window fixed in size.

# Set the tabs in GUI
tabcontrol = ttk.Notebook(root)
tab1 = ttk.Frame(tabcontrol)
tab2 = ttk.Frame(tabcontrol)
tab3 = ttk.Frame(tabcontrol)
tabcontrol.add(tab1, text='Data Uploaded')
tabcontrol.add(tab2, text='Processed Data')
tabcontrol.pack(expand=1, fill="both")

# Frame for TreeView
frame1 = tk.LabelFrame(tab1, text="Excel Data")
frame1.place(height=250, width=700)

frame3 = tk.LabelFrame(tab2, text="Prediction")
frame3.place(height=450, width=700)

# Frame for Graph buttons
frame2 = tk.LabelFrame(tab2, text="Graph")
frame2.place(height=100, width=700, rely=0.7, relx=0)

# Frame for open file dialog
file_frame = tk.LabelFrame(tab1, text="Open File")
file_frame.place(height=300, width=400, rely=0.4, relx=0.2)

# Buttons
button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
button1.place(rely=0.20, relx=0.50)

button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
button2.place(rely=0.20, relx=0.30)

buttonExport = tk.Button(tab2, text="Export File", command=lambda: Export_excel_data())
buttonExport.place(height=35,width=200, rely=0.90, relx=0.33)

buttonGet = tk.Button(file_frame, text="Search", command=lambda: Search())
buttonGet.place(rely=0.56, relx=0.65)

buttonBar = tk.Button(frame2, text="Bar Graph", command=lambda: Bar_Graph())
buttonBar.place(rely=0.30, relx=0.2)

buttonPie = tk.Button(frame2, text="Pie Chart", command=lambda: Pie_chart())
buttonPie.place(rely=0.30, relx=0.45)

buttonDonut = tk.Button(frame2, text="Donut Chart", command=lambda: Donut_chart())
buttonDonut.place(rely=0.30, relx=0.70)

# Take in values entered for Search function
# Entry
label_dst = tk.Label(file_frame, text="Dst Port")
label_dst.place(rely=0.54, relx=0.10)

entry1 = tk.Entry(file_frame)
entry1.place(rely=0.54, relx=0.30)

label_ptl = tk.Label(file_frame, text="Protocol")
label_ptl.place(rely=0.62, relx=0.10)

entry2 = tk.Entry(file_frame)
entry2.place(rely=0.62, relx=0.30)

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

treescrolly2 = tk.Scrollbar(frame3, orient="vertical", command=tv2.yview) # command means update the yaxis view of the widget
treescrollx2 = tk.Scrollbar(frame3, orient="horizontal", command=tv2.xview) # command means update the xaxis view of the widget
tv2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set) # assign the scrollbars to the Treeview Widget
treescrollx2.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly2.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

output = []


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
        tk.messagebox.showerror("Information", f"No available file is found.")
        return None

    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)  # let the column heading = column name

    df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end",
                   values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

    Prediction()


def Export_excel_data():
    """This function will get the data from the Treeview and write it in CSV format, allowing the file to be saved in your file explorer."""
    
    if len(tv2.get_children()) < 1:
        messagebox.showerror("No Data!", "No data available to export")
        return None
    savdia = filedialog.asksaveasfilename(initialdir="/",title="Save File",defaultextension=".csv" ,filetypes=(("CSV File","*.csv"), ("All Files","*")))
    with open(savdia,mode='w') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',')
        exp_writer.writerow(['Prediction', 'Protocol', 'Dst Port',  'Timestamp'])
        for row_id in tv2.get_children():
            row = tv2.item(row_id)["values"]
            exp_writer.writerow(row)

    messagebox.showinfo("Data Exported","Your data has been exported successfully.")


def clear_data():
    """"This function will clear the Treeview"""
    
    tv1.delete(*tv1.get_children())
    return None


def Search():
    """"This function will search according to the text from the entrybox"""
    
    try:
        clear_data()

        df = pd.read_csv(label_file["text"])

        data1 = entry1.get()
        data2 = entry2.get()

        if data1 != "" and data2 != "":
            df_filter = df.loc[df['Dst Port'] == int(data1)]
            df_filter = df_filter.loc[df_filter['Protocol'] == int(data2)]
            df_rows = df_filter.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                tv1.insert("", "end",
                           values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

        elif data1 != "":
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
            tk.messagebox.showerror(title="Invalid", message="Invalid Input")
    except:
        tk.messagebox.showerror(title="File Not Found", message="No files has been selected.")


def Bar_Graph():
    """"This function plots the bar graph as well as displays it"""
    
    if len(tv2.get_children()) < 1:
        messagebox.showerror("No Data!", "No data available to display")
        return None
    else:
        graph_data = pd.DataFrame(np.array(output))
        graph_data.columns = ['Prediction', 'Protocol', 'Dst Port',  'Timestamp']
        
        exclude = ['Benign']
        newdf = graph_data[~graph_data.Prediction.isin(exclude)]

        # Counting each row and converting to list
        x_axis = newdf['Dst Port'].value_counts().keys().tolist()
        y_axsis = newdf['Dst Port'].value_counts().tolist()

        fig, ax = plt.subplots(figsize=(8,5))
        ax.set_title('Number of Attack on Ports', fontsize=22)  # Title of Chart
        ax.set_ylabel('# of Attack')  # Y-Axis label for Bar graph
        ax.set_xlabel('Destination Ports')  # X-Axis label for Bar graph
        ax.bar(x_axis[:5], y_axsis[:5])
        plt.show()


def Pie_chart():
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

        fig, ax = plt.subplots(figsize=(8,5))
        ax.set_title('Number of Each Cyber Attack', fontsize=22)  # Title of Chart

        # Plot of Pie Chart (Consist of All attacks)
        ax.pie(count, autopct=lambda p: '({:.0f})'.format(p * sum(count) / 100), startangle=90)

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.legend(labels=attack)  # Legend for Pie and Donut Chart
        plt.show()

def Donut_chart():
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

        fig, ax = plt.subplots(figsize=(8,5))
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

def Prediction():
    """"This function load the model from Tensorflow and display it"""

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

    combination1 = pd.DataFrame(np.array(output))

    tv2["column"] = ['Prediction', 'Protocol', 'Dst Port', 'Timestamp']
    tv2["show"] = "headings"
    for column in tv2["columns"]:
        tv2.heading(column, text=column)  # let the column heading = column name

    df_rows = combination1.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        tv2.insert("", "end", values=row)

    return output



root.mainloop()
