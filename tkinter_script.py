# Imports and Set-up
from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter
from tkinter import ttk
import tkinter.scrolledtext as tkst
import time
from datetime import datetime
from multiprocessing import Process, Pipe
import multiprocessing
multiprocessing.freeze_support()
import fv_processor
from PIL import ImageTk, Image
import webbrowser
import pandas as pd

intro_text = "This script detects whether two pictures are of the same person. It may be used to help ensure the same person is being interviewed between waves, to detect when someone enrolls more than once in a program, or any other use."
intro_text_p2 = "Though this tool can be helpful, ensuring identity is ultimately still your responsibility."
intro_text_p3 = "*This version is customized for Windows 7. It has limited functionality. It is recommended you use the versions for Windows 10, OSX, or Linux if possible."
app_title = "IPA's Facial Validator - Windows 7*"


class GUI:
    def __init__(self, master):
        self.master = master
        # master.frame(self, borderwidth=4)
        master.title(app_title)
        
        if hasattr(sys, "_MEIPASS"):
            icon_location = os.path.join(sys._MEIPASS, 'IPA-Asia-Logo-Image.ico')
        else:
            icon_location = 'IPA-Asia-Logo-Image.ico'

        master.iconbitmap(icon_location)
        master.minsize(width=686, height=666)

def input(the_message):
    try:
        ttk.Label(frame, text=the_message, wraplength=546, justify=LEFT, font=("Calibri", 11), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 12))

        def evaluate(event=None):
            pass

            #if entry.get() in ['y', 'yes']:
            #    return True
            #res.configure(text="Ergebnis: " + )

    except:  # ## add specific Jupyter error here
        pass

    Label(frame, text="Your Expression:").pack()
    entry = Entry(frame)
    entry.bind("<Return>", evaluate)
    if ttk.Button(frame, text="Submit", command=evaluate, style='my.TButton').pack() is True:
        return True
    entry.pack()
    time.sleep(8)
    res = Label(frame)
    res.pack()
    return ('No')


def tkinter_display(the_message):
    the_message = datetime.now().strftime("%H:%M:%S") + '     ' + the_message
    ttk.Label(frame, text=the_message, wraplength=546, justify=LEFT, font=("Calibri Italic", 11), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 12))
    frame.update()

def file_select():

    dataset_path = askopenfilename()

    tkinter_display('Scroll down for status updates.')
    tkinter_display('The script is running...')

    if __name__ == '__main__':

        tkinter_functions_conn, datap_functions_conn = Pipe()
        tkinter_messages_conn, datap_messages_conn = Pipe()

        ### Importing dataset and printing messages ###
        tkinter_functions_conn.send(dataset_path)

        #p_import = Process(target=PII_data_processor.import_dataset, args=(datap_functions_conn, datap_messages_conn))
        #p_import.start()

        #tkinter_display(tkinter_messages_conn.recv())

        #import_results = tkinter_functions_conn.recv()  # dataset, dataset_path, label_dict, value_label_dict
        #dataset = import_results[0]
        #dataset_path = import_results[1]

        
        ### Main function call ###
        p_initialize = Process(target=fv_processor.read_files, args=(datap_functions_conn, datap_messages_conn))
        p_initialize.start()

        tkinter_display(tkinter_messages_conn.recv())

        #initialize_results = tkinter_functions_conn.recv()
        #identified_pii, restricted_vars = initialize_results[0], initialize_results[1]

        

        ### Fuzzy Partial Stem Match ###
        #if sensitivity.get() == "Medium (Default)":
        #    sensitivity_score = 3
        #elif sensitivity.get() == "Maximum":
        #    sensitivity_score = 5
        #elif sensitivity.get() == "High":
        #    sensitivity_score = 4
        #elif sensitivity.get() == "Low":
        #    sensitivity_score = 2
        #elif sensitivity.get() == "Minimum":
        #    sensitivity_score = 1

    

        #tkinter_display(tkinter_messages_conn.recv())
        

        #root.after(2000, next_steps(identified_pii, dataset, datap_functions_conn, datap_messages_conn, tkinter_functions_conn, tkinter_messages_conn))

def about():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/blob/master/README.md') 

def contact():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/issues')

def source_credit():
    webbrowser.open('http://blog.dlib.net/2017/02/high-quality-face-recognition-with-deep.html')

def comparison():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/blob/master/README.md')

def PII_field_names():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/blob/master/README.md')

def next_steps(identified_pii, dataset, datap_functions_conn, datap_messages_conn, tkinter_functions_conn, tkinter_messages_conn):
    ### Date Detection ###
    p_dates = Process(target=PII_data_processor.date_detection, args=(identified_pii, dataset, datap_functions_conn, datap_messages_conn))
    p_dates.start()

    
    tkinter_display("The results have been exported to: " + str(identified_pii)[1:-1])

    ### Exit Gracefully ###
    tkinter_display('Processing complete. You can use the menu option to restart or exit.')

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    import os
    python = sys.executable
    os.execl(python, python, * sys.argv)


if __name__ == '__main__':

    # GUI

    root = Tk()  # creates GUI window


    my_gui = GUI(root)  # runs code in class GUI

    # Styles
    menubar = tkinter.Menu(root)#.pack()

    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Restart", command=restart_program)
    #filemenu.add_command(label="Save", command=hello)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    # create more pulldown menus
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About (v0.1.0)", command=about)
    helpmenu.add_command(label="- Source", command=source_credit)
    #helpmenu.add_command(label="- Placeholder", command=comparison)
    #helpmenu.add_command(label="- Placeholder", command=PII_field_names)
    #helpmenu.add_command(label="- Placeholder", command=PII_field_names)
    helpmenu.add_separator()
    helpmenu.add_command(label="File Issue on GitHub", command=contact)
    helpmenu.add_separator()
    helpmenu.add_command(label="Contribute", command=contact)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.configure(background='light gray', menu=menubar)
    root.style = ttk.Style()
    # root.style.theme_use("clam")  # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    root.style.configure('my.TButton', font=("Calibri", 11, 'bold'), background='white')
    root.style.configure('my.TLabel', background='white')
    root.style.configure('my.TCheckbutton', background='white')
    root.style.configure('my.TMenubutton', background='white')

    root.resizable(False, False) # prevents window from being resized

    # Display

    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = Canvas(root)
    frame = Frame(canvas, width=606, height=636, bg="white")
    frame.place(x=30, y=30)
    #frame.pack_propagate(False)
    #frame.pack()

    vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((35,30), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    # Instructions

    if hasattr(sys, "_MEIPASS"):
        logo_location = os.path.join(sys._MEIPASS, 'ipa logo.jpg')
    else:
        logo_location = 'ipa logo.jpg'

    logo = ImageTk.PhotoImage(Image.open(logo_location).resize((147, 71), Image.ANTIALIAS)) # Source is 2940 x 1416
    tkinter.Label(frame, image=logo, borderwidth=0).pack(anchor="ne", padx=(0, 30), pady=(30, 0))

    ttk.Label(frame, text=app_title, wraplength=536, justify=LEFT, font=("Calibri", 13, 'bold'), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(30, 10))
    ttk.Label(frame, text=intro_text, wraplength=546, justify=LEFT, font=("Calibri", 11), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 12))
    ttk.Label(frame, text=intro_text_p2, wraplength=546, justify=LEFT, font=("Calibri", 11), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 12))
    ttk.Label(frame, text=intro_text_p3, wraplength=546, justify=LEFT, font=("Calibri", 11), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 30))

    ttk.Label(frame, text="Start Application: ", wraplength=546, justify=LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 10))
    ttk.Button(frame, text="Select Input Sheet", command=file_select, style='my.TButton').pack(anchor='nw', padx=(30, 30), pady=(0, 30))

    ttk.Label(frame, text="Options:", justify=LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 10))

    # Dropdown

    #ttk.Label(frame, text="Select Detection Sensitivity:", justify=LEFT, font=("Calibri", 11), style='my.TLabel').pack(anchor='nw', padx=(30,0))

    #sensitivity = StringVar(frame)
    #w = ttk.OptionMenu(frame, sensitivity, "Medium (Default)", "Maximum", "High", "Medium (Default)", "Low", "Minimum", style='my.TMenubutton').pack(anchor='nw', padx=(30,0))
    # A combobox may be a better choice
    
    # Checkbox

    # checkTemp = IntVar() #IntVar only necessary if need app to change upon being checked
    # checkTemp.set(0)
    # checkCmd.get() == 0 # tests if unchecked, = 1 if checked

    #checkTemp = 1
    #checkBox1 = ttk.Checkbutton(frame, variable=checkTemp, onvalue=1, offvalue=0, text="Output Session Log", style='my.TCheckbutton').pack(anchor='nw', padx=(30, 0), pady=(10,0), fill=X)

    ttk.Label(frame, text="Status:", justify=LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel').pack(anchor='nw', padx=(30,0), pady=(30, 0))
    first_message = "Awaiting dataset selection."
    first_message = datetime.now().strftime("%H:%M:%S") + '     ' + first_message
    ttk.Label(frame, text=first_message, wraplength=546, justify=LEFT, font=("Calibri Italic", 11), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 12))

    # Listener

    root.mainloop()  # constantly looping event listener