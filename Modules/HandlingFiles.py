import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd


def File_dialog(label_file):
    """This Function will open the file explorer and assign the chosen file path to label_file"""

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("Csv Files", "*.csv"), ("All Files", "*.*")))
    label_file["text"] = filename
    return None


def Load_excel_data(label_file, tv1):
    """If the file selected is valid this will load the file into the Treeview"""

    clear_data(tv1)

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


def Export_excel_data(tv2):
    """This function will get the data from the Treeview and write it in CSV format,"""
    """allowing the file to be saved in your file explorer."""

    if len(tv2.get_children()) < 1:
        messagebox.showerror("No Data!", "No data available to export")
        return None
    savdia = filedialog.asksaveasfilename(initialdir="/", title="Save File", defaultextension=".csv",
                                          filetypes=(("CSV File", "*.csv"), ("All Files", "*")))
    with open(savdia, mode='w') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',')
        exp_writer.writerow(['Prediction', 'Protocol', 'Dst Port', 'Timestamp'])
        for row_id in tv2.get_children():
            row = tv2.item(row_id)["values"]
            exp_writer.writerow(row)

    messagebox.showinfo("Data Exported", "Your data has been exported successfully.")


def clear_data(tv1):
    """"This function will clear the Treeview"""

    tv1.delete(*tv1.get_children())
    return None
