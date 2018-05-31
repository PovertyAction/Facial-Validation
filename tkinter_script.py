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

intro_text = "This application detects whether listings of paired pictures are of the same person. It is most often used to help ensure the same person is being interviewed across waves or to detect when someone enrolls more than once in a program. Though this tool can be helpful, ensuring identity is ultimately still your responsibility."
intro_text_p2 = "To use this application you must create an input file according to the template (see help menu). The results will then be output as 'results.csv' to the directory containing your images. Any file with the same name located there will be overwritten. A '1' on the threshold test denotes that the person in the images is the same, while a '0' indicates that they appear not to be."
intro_text_p3 = "This is an alpha program, built without access to studies' participant pictures on which to test or train it. Please help improve this program by filling out the survey on your experience using it (Help -> Provide Feedback)."
app_title = "IPA's Facial Validator - Windows"


class GUI:
    def __init__(self, master):
        self.master = master
        master.title(app_title)
        
        if hasattr(sys, "_MEIPASS"):
            icon_location = os.path.join(sys._MEIPASS, 'IPA-Asia-Logo-Image.ico')
        else:
            icon_location = 'IPA-Asia-Logo-Image.ico'

        master.iconbitmap(icon_location)
        master.geometry('686x666')
        master.minsize(280,200)


def tkinter_display(the_message):
    the_message = datetime.now().strftime("%H:%M:%S") + '     ' + the_message
    ttk.Label(frame, text=the_message, wraplength=546, justify=LEFT, font=("Calibri Italic", 11), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 12))
    frame.update()
    canvas.yview('scroll', '1', 'units')

def file_select():

    dataset_path = askopenfilename()

    tkinter_display('Scroll down for status updates.')
    tkinter_display('Processing...')

    if __name__ == '__main__':

        tkinter_functions_conn, datap_functions_conn = Pipe()
        tkinter_messages_conn, datap_messages_conn = Pipe()

        ### Sending dataset path into Pipe for processor file ###
        tkinter_functions_conn.send(dataset_path)
        
        ### Main function call ###
        p_initialize = Process(target=fv_processor.read_files, args=(datap_functions_conn, datap_messages_conn))
        p_initialize.start()

        tkinter_display(tkinter_messages_conn.recv())
        tkinter_display(tkinter_messages_conn.recv())
        tkinter_display(tkinter_messages_conn.recv())
        tkinter_display(tkinter_messages_conn.recv())

        ### Exit Gracefully ###
        tkinter_display('You can use the file menu to restart or exit.')

def about():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/blob/master/README.md') 

def contact():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/issues')

def source_credit():
    webbrowser.open('http://blog.dlib.net/2017/02/high-quality-face-recognition-with-deep.html')

def template():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/raw/master/input_template.xlsx')

def csv_template():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/blob/master/input_template.csv')

def photo_guidelines():
    webbrowser.open(r'https://github.com/PovertyAction/Facial-Validation/blob/master/Photography%20Guidelines%20for%20Facial%20Validation.pdf')

def comparison():
    webbrowser.open('https://github.com/PovertyAction/Facial-Validation/blob/master/README.md')

def survey():
    webbrowser.open('https://goo.gl/forms/x5wyySTDX1fwcxjv1')

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
    helpmenu.add_command(label="About (v0.2.0)", command=about)
    helpmenu.add_command(label="- Excel Template", command=template)
    helpmenu.add_command(label="- Csv Template", command=csv_template)
    helpmenu.add_command(label="- Source", command=source_credit)
    helpmenu.add_separator()
    helpmenu.add_command(label="Photography Guidelines", command=photo_guidelines)
    helpmenu.add_command(label="File Issue on GitHub", command=contact)
    helpmenu.add_separator()
    helpmenu.add_command(label="Provide Feedback", command=survey)
    #helpmenu.add_command(label="Contribute", command=contact)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.configure(background='light gray', menu=menubar)
    root.style = ttk.Style()
    # root.style.theme_use("clam")  # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    root.style.configure('my.TButton', font=("Calibri", 11, 'bold'), background='white')
    root.style.configure('my.TLabel', background='white')
    root.style.configure('my.TCheckbutton', background='white')
    root.style.configure('my.TMenubutton', background='white')

    root.resizable(True, True) # prevents window from being resized

    # Display

    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = Canvas(root)
    frame = Frame(canvas, width=606, height=636, bg="white")
    frame.place(x=30, y=30)

    vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((35,30), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    #  Building display of app
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
    ttk.Button(frame, text="Select Input File", command=file_select, style='my.TButton').pack(anchor='nw', padx=(30, 30), pady=(0, 30))

    ttk.Label(frame, text="Status:", justify=LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel').pack(anchor='nw', padx=(30,0), pady=(30, 0))
    first_message = "Awaiting dataset selection."
    first_message = datetime.now().strftime("%H:%M:%S") + '     ' + first_message
    ttk.Label(frame, text=first_message, wraplength=546, justify=LEFT, font=("Calibri Italic", 11), style='my.TLabel').pack(anchor='nw', padx=(30, 30), pady=(0, 12))

    # Listener
    root.mainloop()  # constantly looping event listener