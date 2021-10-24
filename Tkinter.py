import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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

buttonExport = tk.Button(file_frame, text="Export File", command=lambda: Export_excel_data())
buttonExport.place(rely=0.65, relx=0.80)

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

    df = df.astype(str)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])  # convert epoch time to datetime
    df["Protocol"].replace({"0": "HOPOPT", "1": "ICMP", "2": "IGMP", "3": "GGP", "4": "IPv4", "5": "ST", "6": "TCP",
                            "7": "CBT", "8": "EGP", "9": "IGP", "10": "BBN-RCC-MON", "11": "NVP-II", "12": "PUP",
                            "13": "ARGUS (deprecated)", "14": "EMCON", "15": "XNET", "16": "CHAOS", "17": "UDP",
                            "18": "MUX", "19": "DCN-MEAS", "20": "HMP", "21": "PRM", "22": "XNS-IDP", "23": "TRUNK-1",
                            "24": "TRUNK-2", "25": "LEAF-1", "26": "LEAF-2", "27": "RDP", "28": "IRTP", "29": "ISO-TP4",
                            "30": "NETBLT", "31": "MFE-NSP", "32": "MERIT-INP", "33": "DCCP", "34": "3PC", "35": "IDPR",
                            "36": "XTP", "37": "DDP", "38": "IDPR-CMTP", "39": "TP++", "40": "IL", "41": "IPv6",
                            "42": "SDRP", "43": "IPv6-Route", "44": "IPv6-Frag", "45": "IDRP", "46": "RSVP",
                            "47": "GRE",
                            "48": "DSR", "49": "BNA", "50": "ESP", "51": "AH", "52": "I-NLSP",
                            "53": "SWIPE (deprecated)", "54": "NARP", "55": "MOBILE", "56": "TLSP", "57": "SKIP",
                            "58": "IPv6-ICMP", "59": "IPv6-NoNxt", "60": "IPv6-Opts", "62": "CFTP", "64": "SAT-EXPAK",
                            "65": "KRYPTOLAN", "66": "RVD", "67": "IPPC", "69": "SAT-MON", "70": "VISA", "71": "IPCV",
                            "72": "CPNX", "73": "CPHB", "74": "WSN", "75": "PVP", "76": "BR-SAT-MON", "77": "SUN-ND",
                            "78": "WB-MON", "79": "WB-EXPAK", "80": "ISO-IP", "81": "VMTP", "82": "SECURE-VMTP",
                            "83": "VINES", "84": "TTP", "84": "IPTM", "85": "NSFNET-IGP", "86": "DGP", "87": "TCF",
                            "88": "EIGRP", "89": "OSPFIGP", "90": "Sprite-RPC", "91": "LARP", "92": "MTP",
                            "93": "AX.25",
                            "94": "IPIP", "95": "MICP (deprecated)", "96": "SCC-SP", "97": "ETHERIP", "98": "ENCAP",
                            "100": "GMTP", "101": "IFMP", "102": "PNNI", "103": "PIM", "104": "ARIS", "105": "SCPS",
                            "106": "QNX", "107": "A/N", "108": "IPComp", "109": "SNP", "110": "Compaq-Peer",
                            "111": "IPX-in-IP", "112": "VRRP", "113": "PGM", "115": "L2TP", "116": "DDX", "117": "IATP",
                            "118": "STP", "119": "SRP", "120": "UTI", "121": "SMP", "122": "SM (deprecated)",
                            "123": "PTP", "124": "ISIS over IPv4", "125": "FIRE", "126": "CRTP", "127": "CRUDP",
                            "128": "SSCOPMCE", "129": "IPLT", "130": "SPS", "131": "PIPE", "132": "SCTP", "133": "FC",
                            "134": "RSVP-E2E-IGNORE", "135": "Mobility Header", "136": "UDPLite", "137": "MPLS-in-IP",
                            "138": "manet", "139": "HIP", "140": "Shim6", "141": "WESP", "142": "ROHC",
                            "143": "Ethernet", }, inplace=True)

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

def Export_excel_data():
    if len(tv1.get_children()) < 1:
        messagebox.showerror("No Data!", "No data available to export")
        return None
    savdia = filedialog.asksaveasfilename(initialdir="/",title="Save File",defaultextension=".csv" ,filetypes=(("CSV File","*.csv"), ("All Files","*")))
    df = pd.read_csv(label_file["text"])
    df = df.astype(str)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])  # convert epoch time to datetime
    df["Protocol"].replace({"0": "HOPOPT", "1": "ICMP", "2": "IGMP", "3": "GGP", "4": "IPv4", "5": "ST", "6": "TCP",
                            "7": "CBT", "8": "EGP", "9": "IGP", "10": "BBN-RCC-MON", "11": "NVP-II", "12": "PUP",
                            "13": "ARGUS (deprecated)", "14": "EMCON", "15": "XNET", "16": "CHAOS", "17": "UDP",
                            "18": "MUX", "19": "DCN-MEAS", "20": "HMP", "21": "PRM", "22": "XNS-IDP", "23": "TRUNK-1",
                            "24": "TRUNK-2", "25": "LEAF-1", "26": "LEAF-2", "27": "RDP", "28": "IRTP", "29": "ISO-TP4",
                            "30": "NETBLT", "31": "MFE-NSP", "32": "MERIT-INP", "33": "DCCP", "34": "3PC", "35": "IDPR",
                            "36": "XTP", "37": "DDP", "38": "IDPR-CMTP", "39": "TP++", "40": "IL", "41": "IPv6",
                            "42": "SDRP", "43": "IPv6-Route", "44": "IPv6-Frag", "45": "IDRP", "46": "RSVP",
                            "47": "GRE",
                            "48": "DSR", "49": "BNA", "50": "ESP", "51": "AH", "52": "I-NLSP",
                            "53": "SWIPE (deprecated)", "54": "NARP", "55": "MOBILE", "56": "TLSP", "57": "SKIP",
                            "58": "IPv6-ICMP", "59": "IPv6-NoNxt", "60": "IPv6-Opts", "62": "CFTP", "64": "SAT-EXPAK",
                            "65": "KRYPTOLAN", "66": "RVD", "67": "IPPC", "69": "SAT-MON", "70": "VISA", "71": "IPCV",
                            "72": "CPNX", "73": "CPHB", "74": "WSN", "75": "PVP", "76": "BR-SAT-MON", "77": "SUN-ND",
                            "78": "WB-MON", "79": "WB-EXPAK", "80": "ISO-IP", "81": "VMTP", "82": "SECURE-VMTP",
                            "83": "VINES", "84": "TTP", "84": "IPTM", "85": "NSFNET-IGP", "86": "DGP", "87": "TCF",
                            "88": "EIGRP", "89": "OSPFIGP", "90": "Sprite-RPC", "91": "LARP", "92": "MTP",
                            "93": "AX.25",
                            "94": "IPIP", "95": "MICP (deprecated)", "96": "SCC-SP", "97": "ETHERIP", "98": "ENCAP",
                            "100": "GMTP", "101": "IFMP", "102": "PNNI", "103": "PIM", "104": "ARIS", "105": "SCPS",
                            "106": "QNX", "107": "A/N", "108": "IPComp", "109": "SNP", "110": "Compaq-Peer",
                            "111": "IPX-in-IP", "112": "VRRP", "113": "PGM", "115": "L2TP", "116": "DDX", "117": "IATP",
                            "118": "STP", "119": "SRP", "120": "UTI", "121": "SMP", "122": "SM (deprecated)",
                            "123": "PTP", "124": "ISIS over IPv4", "125": "FIRE", "126": "CRTP", "127": "CRUDP",
                            "128": "SSCOPMCE", "129": "IPLT", "130": "SPS", "131": "PIPE", "132": "SCTP", "133": "FC",
                            "134": "RSVP-E2E-IGNORE", "135": "Mobility Header", "136": "UDPLite", "137": "MPLS-in-IP",
                            "138": "manet", "139": "HIP", "140": "Shim6", "141": "WESP", "142": "ROHC",
                            "143": "Ethernet", }, inplace=True)
    df.to_csv(savdia, index=False, columns=['Dst Port', 'Protocol', 'Timestamp', 'Label'])

    messagebox.showinfo("Data Exported","Your data has been exported successfully.")
    clear_data()
    label_file["text"] = "No File Selected"

def clear_data():
    # tv1.delete(*tv1.get_children())
    for col in tv1['columns']:
        tv1.heading(col, text='')
    tv1.delete(*tv1.get_children())


root.mainloop()