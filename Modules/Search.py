import tkinter as tk
import pandas as pd
from Modules.HandlingFiles import clear_data


def Search(entry1, entry2, tv1, label_file):
    """"This function will search according to the text from the entrybox"""

    try:
        clear_data(tv1)

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
