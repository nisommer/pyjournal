
#from __future__ import absolute_import
#from __future__ import absolute_import, unicode_literals
#from . import Entry
from tkinter import *
from tkinter import ttk
from datetime import datetime
from datetime import date, timedelta
from tkinter import messagebox
import sys

import Entry
import methods
import json
import jsonpickle
import os
from os.path import expanduser


#import time
from collections import Counter # To count each word ...
__author__ = 'nicolassommer'


# Count words: OK
# Count each word: mostly OK

## TODO:
## Save text in some way

## Get a calendar view, and assign each text box to its calendar day. (or simply, when changing calendar
#save the current day's text, and reload a new day's text.
#- check if day exists or not -> create new text ...
#I should probably have a method to check the most recent entry in the Calendar ..


def retrieve_input():
    return text.get("1.0", "end-1c")

def on_closing():
    if messagebox.askyesno("Save", "Do you want to save?"):
        return_touched()
    root.destroy()

def key_touched(*args):

    """
    Update when a key is typed
    :param args:
    """

    # Display time since last keystroke
    global last_touch
    delta=(datetime.now()-last_touch)
    #global initTime
    #print("{}min {}s".format(int(delta.seconds/60),delta.seconds%60))
    last_touch = datetime.now()
    origindate=datetime(2000, 1, 1, 00, 00, 0)
    print((origindate+delta).strftime("%H:%M:%S"))

    # Time since last touch
    deltaInit=datetime.now()-initTime
    # Update time since beginning
    lastTimeText.set((origindate+deltaInit).strftime("%H:%M:%S"))


    input_str = retrieve_input()
    nwords = len(input_str.split())
    wordCount.set(nwords)
    wordsText.set(str(nwords) + " words")
    counts = Counter(input_str.lower().split()) # Need a way to transform this list in another way ...
    #cnames.set(tuple(counts.items())) # Old version, this is quite better.

    wordList = []
    wordSet=set()
    for key, value in counts.items():
        wordSet.add((str(value) + ": " + str(key)))
        wordList.append((str(value) + ": " + str(key)))

    wordList.sort(reverse=1)
    cnames.set(tuple(wordList))


    # Try to print out the current line ..
    # print(text.get("insert linestart","insert lineend")=="")
    # if(text.get("insert linestart","insert lineend").strip()==""):
    #     print("empty line")
    # else:
    #     print("There is something on the line")

def return_touched(*args):

    """
    Update when a return is typed. Goal is to save the data here ...
    :param args:
    """

    input_str = retrieve_input()
    newentry = methods.new_entry(input_str, currentdate)

    # jsondump = jsonpickle.encode(newentry)
    #
    # myfile = open(journal_file,"w")
    # myfile.write(jsondump)
    # myfile.close()

    my_entries[str(newentry.date)] = newentry
    print("my_entries length: " + str(len(my_entries.keys())))

    # For several entries
    jsondump_entries = jsonpickle.encode(my_entries)
    myfile_entries = open(journal_file_entries,"w")
    myfile_entries.write(jsondump_entries)
    myfile_entries.close()

def display_info():
    # Probably there is a better way than to create everything here, it should just appear...
    t = Toplevel(root)
    t.geometry('300x200+'+str(root.winfo_width()+root.winfo_x()+20)+'+'+str(root.winfo_y())) # Set it next to the initial window
    root.winfo_geometry()
    root.wm_geometry()

    input_str = retrieve_input()

    lbox = Listbox(t, listvariable=cnames, height=5)
    lbox.pack(fill=BOTH,expand=1)


def dateset(direction):
    # Save the shit
    return_touched()

    global currentdate
    if direction=="right":
        currentdate = currentdate + timedelta(days=1)
    elif direction == "left":
        currentdate = currentdate + timedelta(days=-1)
    else:
        currentdate = date.today()


    dateload(currentdate)
    key_touched()



def dateload(date):
    text.delete(1.0,END)
    if (str(date) in my_entries):
        text.insert(1.0, my_entries[str(date)].body)
    else:
        text.insert(1.0,"")
    # Set new date on top ...
    dateDisplayText.set(currentdate.strftime("%A %d %b %Y"))


def insertTime():

    stringtemp = "\n--- TIME: " + datetime.today().strftime("%H:%M")  +"---"

    if(text.get("insert linestart","insert lineend").strip()==""):
        print("empty line")
    else:
        print("There is something on the line")
        stringtemp+="\n"

    text.insert("insert linestart", stringtemp)








### MAIN code

root = Tk()
root.title("Journal test program")

initTime=datetime.now()

# Previous version ...
mainframe = ttk.Frame(root)
mainframe.pack(fill=BOTH,expand=1)

## Create Main Frame
text = Text(mainframe,background = "light yellow",wrap="word")

bottomframe = ttk.Frame(root)
quitButton = Button(bottomframe, text="QUIT", command=root.destroy)
infoButton = Button(bottomframe, text="Info", command=display_info)
TagButton = Button(bottomframe, text="Tag time", command=insertTime)



wordCount = IntVar() # Number of words
wordsText = StringVar() # Contents of the text widget
words = Label(mainframe,textvariable=wordsText,background="grey")
wordsText.set("0 words")

# Top bar
topframe = ttk.Frame(mainframe)
dateDisplayText = StringVar()
dateDisplay = Label(topframe,textvariable=dateDisplayText, background="grey")
rightbutton = Button(topframe,text=">" ,command=lambda: dateset("right"))
leftbutton = Button(topframe,text="<", command=lambda: dateset("left"))
homebutton = Button(topframe,text="HOME", command=lambda: dateset("home"))

rightbutton.pack(side=RIGHT)
homebutton.pack(side=RIGHT)
leftbutton.pack(side=RIGHT)
TagButton.pack(side=RIGHT)

progressbar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=200, mode='determinate', maximum = 750, variable=wordCount)

lastTimeText=StringVar()
lastTimeDisplay = Label(mainframe,textvariable=lastTimeText,background="grey")
lastTimeText.set("00:00:00")
# Actually, it would be much better to update this every second ... now it does not make sense ...


dateDisplay.pack(side=TOP,fill=BOTH)

topframe.pack(side=TOP,fill=BOTH)

text.pack(side=TOP,fill=BOTH)
bottomframe.pack(side=BOTTOM)
words.pack(side=RIGHT)
lastTimeDisplay.pack(side=LEFT)
progressbar.pack(side=LEFT,expand=1,fill = X)

quitButton.pack(side = LEFT)
infoButton.pack(side = RIGHT)

# Set focus on the text area
text.focus_set()

cnames = StringVar() # Used to display words in the new window

# Starting some inits
last_touch = datetime.now()

global currentdate
currentdate= date.today()

nowH = datetime.today()
#.set(nowH.strftime("%A %d %b %Y, %H:%M"))
dateDisplayText.set(currentdate.strftime("%A %d %b %Y"))
# Get dropbox's location
if(sys.platform.startswith("linux")):
    dropbox_config_path = expanduser("~") + "/.dropbox/info.json"
elif(sys.platform.startswith("darwin")):
    dropbox_config_path = expanduser("~") + "/.dropbox/info.json"
elif(sys.platform.startswith("win")):
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
journal_file = dropbox_folder_path+'/.journal.txt'
journal_file_entries = dropbox_folder_path+'/.entries.txt'

# # Load 1 entry
# try:
#     myfile = open(journal_file)
#     #myfile = open('data.txt')
#     jsondump = myfile.read()
#     #print("read from last time: " +jsondump)
#     myEntry = jsonpickle.decode(jsondump)
# except:
#     print("File not found, not loading anything ...")

# Load all entries
try:
    myfile_entries = open(journal_file_entries)
    jsondump_entries = myfile_entries.read()
    my_entries = jsonpickle.decode(jsondump_entries)
    dateload(currentdate)

except:
    print("entries file not found, Creating a new file ...")
    my_entries = dict()



# Init the functions
key_touched()

# Set bindings
root.bind('<KeyPress>', key_touched)
root.bind('<Return>', return_touched)

# Run the program
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()