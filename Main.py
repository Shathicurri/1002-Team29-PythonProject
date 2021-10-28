import tkinter as tk
from tkinter import ttk

from Modules.MyPrediction import Prediction
from Modules.Graphs import Donut_chart, Bar_Graph, Pie_chart
from Modules.Search import Search
from Modules.HandlingFiles import File_dialog, Load_excel_data, Export_excel_data

# initalise the tkinter GUI
root = tk.Tk()

root.title("Digital Crime Analyzer") # title of application
root.geometry("700x700")  # set the root dimensions
root.pack_propagate(False)  # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0)  # makes the root window fixed in size.

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
button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog(label_file))
button1.place(rely=0.20, relx=0.50)

button2 = tk.Button(file_frame, text="Load File", command=lambda: Loading_data(label_file, tv1, tv2))
button2.place(rely=0.20, relx=0.30)

buttonExport = tk.Button(tab2, text="Export File", command=lambda: Export_excel_data(tv2))
buttonExport.place(height=35, width=200, rely=0.90, relx=0.33)

buttonGet = tk.Button(file_frame, text="Search", command=lambda: Search(entry1, entry2, tv1, label_file))
buttonGet.place(rely=0.56, relx=0.65)

buttonBar = tk.Button(frame2, text="Bar Graph", command=lambda: Bar_Graph(output, tv2))
buttonBar.place(rely=0.30, relx=0.2)

buttonPie = tk.Button(frame2, text="Pie Chart", command=lambda: Pie_chart(output, tv2))
buttonPie.place(rely=0.30, relx=0.45)

buttonDonut = tk.Button(frame2, text="Donut Chart", command=lambda: Donut_chart(output, tv2))
buttonDonut.place(rely=0.30, relx=0.70)

# Take in values entered for Search function
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
tv1.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame1, orient="vertical",
                           command=tv1.yview)  # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                           command=tv1.xview)  # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set,
              yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

tv2 = ttk.Treeview(frame3)
tv2.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

treescrolly2 = tk.Scrollbar(frame3, orient="vertical",
                            command=tv2.yview)  # command means update the yaxis view of the widget
treescrollx2 = tk.Scrollbar(frame3, orient="horizontal",
                            command=tv2.xview)  # command means update the xaxis view of the widget
tv2.configure(xscrollcommand=treescrollx2.set,
              yscrollcommand=treescrolly2.set)  # assign the scrollbars to the Treeview Widget
treescrollx2.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
treescrolly2.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

output = []


def Loading_data(label_file, tv1, tv2):
    Load_excel_data(label_file, tv1)
    if label_file["text"] != "No File Selected":
        combo = Prediction(label_file, tv2)
        for i in combo:
            output.append(i)


root.mainloop()
