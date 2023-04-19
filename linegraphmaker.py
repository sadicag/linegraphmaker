from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
from tkinter import filedialog
from tkinter import simpledialog
import os
import numpy as np
import matplotlib.pyplot as plt
import py_compile

# CONSTANTS FOR THE GM_SETTINGS FILE
s_lgnd = "LEGENDS-SIZE"
s_mnr  = "MINOR-TICKS"
s_grid = "GRAPH-GRID"
s_ttl  = "GRAPH-TITLE" 
s_xtxt = "X-AXIS-TEXT"
s_ytxt = "Y-AXIS-TEXT"
s_xaxs = "X-AXIS-FILE"
s_yaxs = "Y-AXIS-FILE"
s_name = "FILE-NAME"

# TKINTER INITIALIZATION
root            = Tk()
#root.geometry("350x380")
root.title('Line Graph Maker')
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
x_path_t = ttk.Label(mainframe, text=" ")
y_listbox_t = Listbox(mainframe, width=100)
y_remove_entry = ttk.Entry(mainframe, width=20)
legendsize_entry = ttk.Entry(mainframe, width=5)

# CONSTANTS FOR GUI INTERFACE
filename_t      = StringVar()
graphtitle_t    = StringVar()
yaxis_t         = StringVar()
xaxis_t         = StringVar()
minorticks_t    = IntVar()
graphgrid_t     = IntVar()
x               = []
y_list          = []
y_label_list    = []
y_fn_list       = []

def print_warning(str):
    print('WARNING: ' + str)

def print_status(str):
    print('\tSTATUS: ' + str)

def str_to_int(str):
    return int((str.replace('\n', '')).replace('\r', ''))

def str_to_float(str):
    return float((str.replace('\n', '')).replace('\r', ''))

def read_data_from_path(filepath):
    data = open(filepath, "r")
    print_status('FILE ' + filepath + ' FOUND')
    file = data.readlines()
    list = []
    for line in file:
        n = str_to_float(line)
        list.append(n)
    return list

def normalize_string(str):
    return str.replace('\n', '').replace('\r', '')

def string_to_filename(str):
    return normalize_string(str).replace(' ', '_')

def fix_y_length(y, size):
    if len(y) < size:
        print_warning('Y-LENGTH IS SMALLER THAN X-LENGTH')
        dif = size - len(y)
        print_warning('FILLING Y WITH '+str(dif)+' ZEROS')
        n_list = [0] * dif
        return y + n_list 
    if size < len(y):
        print_warning('Y-LENGTH BIGGER THAN X-LENGTH')
        print_warning('TRIMMING Y TO LENGTH '+str(len(y)-size))
        return y[:size]
    return y

def create_graph():
    global filename_t
    global graphtitle_t
    global xaxis_t
    global yaxis_t
    global minorticks_t
    global graphgrid_t
    global x
    global y_list
    global y_label_list
    global legendsize_entry

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['figure.dpi'] = 360
    plt.rcParams["figure.autolayout"] = True
    
    # GRAPH MINOR TICKS
    if (minorticks_t.get() == 1):
        plt.minorticks_on()

    # GRAPH GRID
    if (graphgrid_t.get() == 1):
        plt.grid()

    # GRAPH TITLE
    plt.title(graphtitle_t.get())

    # VALIDATE X-AXIS
    if (len(x) == 0):
        print_warning('X-AXIS IS EMPTY')

    # CHANGE AXIS TEXT
    plt.xlabel(xaxis_t.get())
    plt.ylabel(yaxis_t.get())

    # PLOT ALL DATA
    for i in range(0, len(y_list)):
        y = y_list[i]
        y_label = y_label_list[i]
        plt.plot(x, fix_y_length(y, len(x)), label=y_label)
 
    # LEGEND SIZE
    plt.legend()
    if (len(legendsize_entry.get()) > 0):
        plt.legend(prop={'size' : int(legendsize_entry.get())})
    else:
        plt.legend(prop={'size' : 7})

    # SAVE FILE
    filename = 'my_graph.png'
    if len(filename_t.get()) > 0:
        filename = string_to_filename(filename_t.get())
    plt.savefig(filename)
    print('GRAPH HAS BEEN SAVED AS ' + filename)
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


def on_closing():
    global root
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def import_xaxis_data():
    global x
    global x_path_t
    filename = filedialog.askopenfilename()
    x = read_data_from_path(filename)
    if (len(x)>0):
        x_path_t.configure(text=filename)

def refresh_y_list():
    global y_list
    global y_label_list
    global y_listbox_t
    global y_fn_list
    y_listbox_t.delete(0, END)
    for i in range(0, len(y_list)):
        txt = str(i) + ' | '
        if (y_label_list[i] == "" or y_label_list[i] == " " or y_label_list[i] == "\n" or y_label_list[i] == "\t"):
            txt = txt + y_fn_list[i]
        else:
            txt = txt + y_label_list[i]
        y_listbox_t.insert(END, txt)

def import_yaxis_data():
    global y_list
    global y_label_list
    global y_fn_list
    global y_listbox_t
    filename = filedialog.askopenfilename()
    y = read_data_from_path(filename)
    y_label = simpledialog.askstring(title = "Y-Axis Label", prompt="Enter a Label for the imported Y-Axis (Optional)")
    y_label_list.append(y_label)
    y_list.append(y)
    y_fn_list.append(filename)
    
    refresh_y_list()

def remove_y_key():
    global y_list
    global y_label_list
    global y_fn_list
    global y_remove_entry
    if (len(y_remove_entry.get()) > 0):
        key = int(y_remove_entry.get())
        del y_list[key]
        del y_label_list[key]
        del y_fn_list[key]
        refresh_y_list()

def gui_interface():
    root.columnconfigure(4, weight=1)
    root.rowconfigure(4, weight=1)
    
    # FILENAME STRING INPUT
    ttk.Label(mainframe, text="Filename").grid(column=1, row=1, sticky=(W, E))
    filename_entry = ttk.Entry(mainframe, width=5, textvariable=filename_t)
    filename_entry.grid(column=2, row=1, sticky=(W,E))
   
    # GRAPH TITLE STRING INPUT
    ttk.Label(mainframe, text="Title").grid(column=1, row=2, sticky=(W, E))
    graphtitle_entry = ttk.Entry(mainframe, width=5, textvariable=graphtitle_t)
    graphtitle_entry.grid(column=2,row=2, sticky=(W,E))

    # X-AXIS TEXT STRING INPUT
    ttk.Label(mainframe, text="X-Axis Title").grid(column=1, row=3, sticky=(W, E))
    xaxis_entry = ttk.Entry(mainframe, width=5, textvariable=xaxis_t)
    xaxis_entry.grid(column=2,row=3, sticky=(W,E))
    
    # Y-AXIS TEXT STRING INPUT
    ttk.Label(mainframe, text="Y-Axis Title").grid(column=1, row=4, sticky=(W, E))
    yaxis_entry = ttk.Entry(mainframe, width=5, textvariable=yaxis_t)
    yaxis_entry.grid(column=2,row=4, sticky=(W,E))

    # LEGENDSIZE INTEGER INPUT
    global legendsize_entry
    ttk.Label(mainframe, text="Legend Size").grid(column=1, row=5, sticky=(W, E))
    legendsize_entry.grid(column=2,row=5, sticky=(W,E))

    # MINOR TICKS CHECKBOX
    ttk.Checkbutton(mainframe, text="Graph Minor Ticks", variable=minorticks_t).grid(column=3 ,row=1, sticky=(W, E))

    # GRAPH-GRID CHECKBOX
    ttk.Checkbutton(mainframe, text="Graph Grid", variable=graphgrid_t).grid(column=3 ,row=2, sticky=(W, E))

    # X-AXIS DATA IMPORT
    global x_path_t
    ximport = ttk.Button(mainframe, text="Import X-Axis", command=import_xaxis_data).grid(column=1, row=7, sticky=(W, E))
    x_path_t.configure(text="FILE PATH")
    x_path_t.grid(column=2, row=7, sticky=(W, E))

    # Y-AXIS DATA IMPORT
    yimport = ttk.Button(mainframe, text="Import Y-Axis", command=import_yaxis_data).grid(column=1, row=8, sticky=(W, E))

    # Y-AXIS REMOVE WITH KEY
    global y_remove_entry
    yaxisremove = ttk.Button(mainframe, text="Remove Y-Axis", command=remove_y_key).grid(column=2,row=8, sticky=(W, E))
    y_remove_entry.grid(column=3,row=8, sticky=(W, E))

    # Y-AXIS LISTBOX
    global y_listbox_t
    y_listbox_t.grid(column=1, columnspan=3, row=9, sticky=(W, E))

    # CREATE GRAPH BUTTON
    ttk.Button(root, text="Create Graph", command=create_graph).grid(sticky=(W, E)) 

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    

def main():
    gui_interface()
    #create_graph_from_settings()

if __name__ == "__main__":
    main()


