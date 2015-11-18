# from __future__ import absolute_import
# from __future__ import absolute_import, unicode_literals
# from . import Entry
from tkinter import *
from tkinter import ttk
from datetime import datetime
from datetime import date, timedelta
from tkinter import messagebox
import json
import os
from os.path import expanduser

import sys
import atexit
import methods
import jsonpickle





# import time
from collections import Counter  # To count each word ...

__author__ = 'nicolassommer'


# Count words: OK
# Count each word: mostly OK

## TODO:

## Get a calendar view, and assign each text box to its calendar day. (or simply, when changing calendar
# save the current day's text, and reload a new day's text.
# - check if day exists or not -> create new text ...
# I should probably have a method to check the most recent entry in the Calendar ..


def update_time():
    global last_touch
    last_touch = datetime.now()
    origindate = datetime(2000, 1, 1, 00, 00, 0)

    # Time since last touch
    deltaInit = datetime.now() - initTime
    # Update time since beginning
    lastTimeText.set((origindate + deltaInit).strftime("%H:%M:%S"))
    root.after(1000, update_time)


def retrieve_input():
    return text.get("1.0", "end-1c")


def on_closing():
    if messagebox.askyesno("Save", "Do you want to save?"):
        SaveEntry()
    root.destroy()


def CountWords(*args):
    """
    Update when a key is typed
    :param args:
    """

    input_str = retrieve_input()
    nwords = len(input_str.split())
    wordCount.set(nwords)
    wordsText.set(str(nwords) + " words")
    counts = Counter(input_str.lower().split())  # Need a way to transform this list in another way ...

    wordList = []
    for key, value in counts.items():
        wordList.append((str(value) + ": " + str(key)))

    wordList.sort(reverse=1)
    cnames.set(tuple(wordList))


def SaveEntry(*args):
    """
    Update when a return is typed. Goal is to save the data here ...
    :param args:
    """

    input_str = retrieve_input()
    newentry = methods.new_entry(input_str, currentdate)


    my_entries[str(newentry.date)] = newentry
    print("my_entries length (entries): " + str(len(my_entries.keys())))

    # For several entries
    jsondump_entries = jsonpickle.encode(my_entries)
    myfile_entries = open(journal_file_entries, "w")
    myfile_entries.write(jsondump_entries)
    myfile_entries.close()


def display_info():
    # Probably there is a better way than to create everything here, it should just appear...
    t = Toplevel(root)
    t.geometry('300x200+' + str(root.winfo_width() + root.winfo_x() + 20) + '+' + str(
        root.winfo_y()))  # Set it next to the initial window

    lbox = Listbox(t, listvariable=cnames, height=5)
    lbox.pack(fill=BOTH, expand=1)


def ChangeDay(direction):
    # Save the text
    SaveEntry()

    global currentdate
    if direction == "right":
        currentdate = currentdate + timedelta(days=1)
    elif direction == "left":
        currentdate = currentdate + timedelta(days=-1)
    else:
        currentdate = date.today()

    dateload(currentdate)

    # Do the usual computation
    CountWords()


def dateload(date):
    text.delete(1.0, END)
    if (str(date) in my_entries):
        text.insert(1.0, my_entries[str(date)].body)
    else:
        text.insert(1.0, "")
    # Set new date on top ...
    dateDisplayText.set(currentdate.strftime("%A %d %b %Y"))

    # Change position of the cursor to end of file.
    text.mark_set(INSERT, END)
    # Scroll to desired position
    text.see(INSERT)
    # Set focus on the text area (ready to write)
    text.focus_set()


def insertTime():
    stringtemp = "--- TIME: " + datetime.today().strftime("%H:%M") + "---"

    if (text.get("insert linestart", "insert lineend").strip() == ""):
        print("empty line")
    else:
        print("There is something on the line")

    stringtemp += "\n"

    text.insert("insert linestart", stringtemp)





### MAIN init code

root = Tk()
root.title("Journal test program")

initTime = datetime.now()

# Previous version ...
mainframe = ttk.Frame(root)
mainframe.pack(fill=BOTH, expand=1)

## Create Main Frame
# text = Text(mainframe,background = "light yellow",wrap="word",yscrollcommand=True)
text = Text(mainframe, background="light yellow", wrap="word")


bottomframe = ttk.Frame(root)
quitButton = Button(bottomframe, text="QUIT", command=on_closing)
infoButton = Button(bottomframe, text="Info", command=display_info)
TagButton = Button(bottomframe, text="Tag time", command=insertTime)

wordCount = IntVar()  # Number of words
wordsText = StringVar()  # Contents of the text widget
words = Label(mainframe, textvariable=wordsText, background="grey")
wordsText.set("0 words")

# Top bar
topframe = ttk.Frame(mainframe)
dateDisplayText = StringVar()
dateDisplay = Label(topframe, textvariable=dateDisplayText, background="grey")
rightbutton = Button(topframe, text=">", command=lambda: ChangeDay("right"))
leftbutton = Button(topframe, text="<", command=lambda: ChangeDay("left"))
homebutton = Button(topframe, text="HOME", command=lambda: ChangeDay("home"))

rightbutton.pack(side=RIGHT)
homebutton.pack(side=RIGHT)
leftbutton.pack(side=RIGHT)
TagButton.pack(side=RIGHT)

progressbar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=200, mode='determinate', maximum=750,
                              variable=wordCount)

lastTimeText = StringVar()
lastTimeDisplay = Label(mainframe, textvariable=lastTimeText, background="grey")
lastTimeText.set("00:00:00")
# Actually, it would be much better to update this every second ... now it does not make sense ...


dateDisplay.pack(side=TOP, fill=BOTH)

topframe.pack(side=TOP, fill=BOTH)

text.pack(side=TOP, fill=BOTH, expand=1)
bottomframe.pack(side=BOTTOM)
words.pack(side=RIGHT)
lastTimeDisplay.pack(side=LEFT)
progressbar.pack(side=LEFT, expand=1, fill=X)

quitButton.pack(side=LEFT)
infoButton.pack(side=RIGHT)

cnames = StringVar()  # Used to display words in the new window

# Starting some initializations
last_touch = datetime.now()

global currentdate
currentdate = date.today()

nowH = datetime.today()
dateDisplayText.set(currentdate.strftime("%A %d %b %Y"))

# Get dropbox's location
if (sys.platform.startswith("linux")):
    dropbox_config_path = expanduser("~") + "/.dropbox/info.json"
elif (sys.platform.startswith("darwin")):
    dropbox_config_path = expanduser("~") + "/.dropbox/info.json"
elif (sys.platform.startswith("win")):
    dropbox_config_path = os.getenv('APPDATA') + "\Dropbox\info.json"
else:
    print("Failed to get Dropbox's config file path")

print("dropbox_config_path: " + dropbox_config_path)
try:
    dropbox_config_file = open(dropbox_config_path)
except:
    print("failed opening Dropbox's config file")

dropbox_config_content = dropbox_config_file.read()
dropbox_config_json = json.loads(dropbox_config_content)
dropbox_folder_path = dropbox_config_json["personal"]["path"]
print("dropbox_path: " + dropbox_folder_path)
journal_file = dropbox_folder_path + '/.journal.txt'
journal_file_entries = dropbox_folder_path + '/.entries.txt'


# Load all entries
try:
    myfile_entries = open(journal_file_entries)
    jsondump_entries = myfile_entries.read()
    my_entries = jsonpickle.decode(jsondump_entries)
    dateload(currentdate)

except:
    # Seems that it enters here, not sure why ...
    print("entries file not found, Creating a new file ...")
    my_entries = dict()


# Change Theme
s = ttk.Style()
print(s.theme_names())
print(s.theme_use())
s.theme_use("clam")  # Not sure that works on windows !

# Put the window on top. Some additional content if mac
root.lift()
if (sys.platform.startswith("darwin")):
    os.system(''' /usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')


# Init the functions
CountWords()

# Set bindings
root.bind('<KeyPress>', CountWords)
root.bind('<Return>', SaveEntry)
# Bind Alt-arrow to change the day
root.bind('<Mod2-Left>', lambda a: ChangeDay("left"))
root.bind('<Mod2-Right>', lambda a: ChangeDay("right"))
root.bind('<Mod2-Up>', lambda a: ChangeDay("home"))


# Do a save check on the exit
# root.protocol("WM_DELETE_WINDOW", on_closing)
# This version runs on mac too.
atexit.register(on_closing)
root.after(1000, update_time)

# Run the program
root.mainloop()




# TODO:
# Add a second screen or something similar ?
# Correct tag behaviour (new line, etc.)
# Enable more bindings (undo/redo, next/previous day, select all)
# Proper resizing of the elements (+min size)
# Check all themes on each platform
root.mainloop()


# py2applet --make-setup JournalPack.py
# python3.4 setup.py py2app
