
#from __future__ import absolute_import
#from __future__ import absolute_import, unicode_literals
#from . import Entry
from tkinter import *
from tkinter import ttk
from datetime import datetime

import Entry
import methods
import json
import jsonpickle
import os

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

def return_touched(*args):

    """
    Update when a return is typed. Goal is to save the data here ...
    :param args:
    """

    print("test")
    input_str = retrieve_input()
    newentry = methods.new_entry(input_str)
    # Print to unicode
    #print(newentry.__unicode__())
    # Print to json (trial 1) but harder to get back from the string afterwards !
    #print(json.dumps(newentry.to_dict()))

    jsondump = jsonpickle.encode(newentry)
    print("json dump:" + jsondump)



    myfile = open(journal_file,"w")
    #myfile = open('data.txt', 'w')
    myfile.write(jsondump)
    myfile.close()


    # I will need a way to read from json too ...
    #print(jsonpickle.encode(newentry))
    #recreated = jsonpickle.decode(jsonpickle.encode(newentry))
    #print(type(recreated))
    #print("body: " + recreated.body)
    #print(recreated.body)


    # Here create a new Entry, and print that Entry ...




def display_info():
    # Probably there is a better way than to create everything here, it should just appear...
    t = Toplevel(root)
    t.geometry('300x200+'+str(root.winfo_width()+root.winfo_x()+20)+'+'+str(root.winfo_y())) # Set it next to the initial window
    print(root.aspect)
    root.winfo_geometry()
    root.wm_geometry()
    print(root.winfo_width()+root.winfo_x())

    input_str = retrieve_input()

    lbox = Listbox(t, listvariable=cnames, height=5)
    lbox.pack(fill=BOTH,expand=1)



### MAIN code

root = Tk()
root.title("Journal test program")


initTime=datetime.now()


# Previous version ...
mainframe = ttk.Frame(root)
mainframe.pack(fill=BOTH,expand=1)


## Create Main Frame
text = Text(mainframe)

bottomframe = ttk.Frame(root)
quitButton = Button(bottomframe, text="QUIT", command=root.destroy)
infoButton = Button(bottomframe, text="Info", command=display_info)

wordCount = IntVar() # Number of words
wordsText = StringVar() # Contents of the text widget
words = Label(mainframe,textvariable=wordsText,background="grey")
wordsText.set("0 words")

dateDisplayText = StringVar()
dateDisplay = Label(mainframe,textvariable=dateDisplayText,background="grey")
nowH = datetime.today()
dateDisplayText.set(nowH.strftime("%A %d %b %Y, %H:%M"))

progressbar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=200, mode='determinate', maximum = 750, variable=wordCount)

lastTimeText=StringVar()
lastTimeDisplay = Label(mainframe,textvariable=lastTimeText,background="grey")
lastTimeText.set("00:00:00")
# Actually, it would be much better to update this every second ... now it does not make sense ...


dateDisplay.pack(side=TOP,fill=BOTH)
text.pack(side=TOP,fill=BOTH)
bottomframe.pack(side=BOTTOM)
words.pack(side=RIGHT)
lastTimeDisplay.pack(side=LEFT)
progressbar.pack(side=LEFT,expand=1,fill = X)

quitButton.pack(side=LEFT)
infoButton.pack(side = RIGHT)

# Set focus on the text area
text.focus_set()

cnames = StringVar() # Used to display words in the new window
last_touch = datetime.now()


# Get dropbox's location
dropbox_config_file = open(os.getenv('APPDATA') + "\Dropbox\info.json")
test = dropbox_config_file.read()
data = json.loads(test)
dropbox_path = data["personal"]["path"]
print("dropbox_path: " + dropbox_path)
journal_file = dropbox_path+'.journal.txt'


# Load data
try:
    myfile = open(journal_file)
    #myfile = open('data.txt')
    jsondump = myfile.read()
    #print("read from last time: " +jsondump)
    myEntry = jsonpickle.decode(jsondump)
    text.insert("1.0", myEntry.body)
except:
    print("File not found, not loading anything ...")

print(os.getenv('APPDATA'))





# Set bindings
root.bind('<KeyPress>', key_touched)
root.bind('<Return>', return_touched)

# Run the program
root.mainloop()