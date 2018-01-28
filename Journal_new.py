# !/usr/bin/env python

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


from collections import Counter  # To count each word ...

__author__ = 'nicolassommer'


# Count words: OK
# Count each word: mostly OK

# TODO:

# -- Primary
# Some functions take *args as second argument, and I don't remember why.

# Filter the "info" function to remove some useless words (stopwords).
# I could use a library made for that, but that's a bit too much


# -- Secondary
# Get a calendar view, and assign each text box to its calendar day. (or simply, when changing calendar
# save the current day's text, and reload a new day's text.
# - check if day exists or not -> create new text ...
# I should probably have a method to check the most recent entry in the Calendar ..


# Add a second screen or something similar ?
# Correct tag behaviour (new line, etc.)
# Enable more bindings (undo/redo, next/previous day, select all)
# Proper resizing of the elements (+min size)
# Check all themes on each platform

class Journal():
    """Journal class"""

    def __init__(self):
        """Initialize windows and variables"""

        self.prepare_windows()

        self.l_word_count = StringVar()  # Used to display words in the new window

        # Starting some initializations
        self.last_touch = datetime.now()
        self.currentdate = date.today()
        self.dateDisplayText.set(self.currentdate.strftime("%A %d %b %Y"))

        # LOAD DATA
        self.find_dropbox_path()
        self.load_entries()

        ##  Change Theme
        # s = ttk.Style()
        # Print available themes.
        # print(s.theme_names())
        # themes = ('aqua', 'clam', 'alt', 'default', 'classic')
        # s.theme_use("")
        # s.theme_use(themes[4])  # Not sure that works on windows !
        # print(s.theme_use())

        # Init the functions
        self.CountWords()

        # Do a save check on the exit
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # This version runs on mac too:

        # Run "update_time" every second
        atexit.register(self.on_closing)
        self.root.after(1000, self.update_time)

        # # Run the program
        self.root.mainloop()

    def prepare_windows(self):
        # Initialize the windows and buttons
        self.root = Tk()
        self.root.title("Journal")

        self.initTime = datetime.now()

        # Previous version ...
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.pack(fill=BOTH, expand=1)

        # Create Main Frame
        self.text = Text(self.mainframe, background="light yellow", wrap="word")

        bottomframe = ttk.Frame(self.root)
        quitButton = Button(bottomframe, text="QUIT", command=self.on_closing)
        infoButton = Button(bottomframe, text="Info", command=self.display_info)
        TagButton = Button(bottomframe, text="Tag time", command=self.insertTime)

        self.wordCount = IntVar()  # Number of words
        self.wordsText = StringVar()  # Contents of the text widget
        words = Label(self.mainframe, textvariable=self.wordsText, background="grey")
        self.wordsText.set("0 words")

        # Top bar
        topframe = ttk.Frame(self.mainframe)
        self.dateDisplayText = StringVar()
        dateDisplay = Label(
            topframe, textvariable=self.dateDisplayText, background="grey")

        rightbutton = Button(topframe, text=">", command=lambda: self.ChangeDay("right"))
        rightbutton2 = Button(topframe, text=">>",
                              command=lambda: self.ChangeDay("right2"))
        leftbutton = Button(topframe, text="<", command=lambda: self.ChangeDay("left"))
        leftbutton2 = Button(topframe, text="<<", command=lambda: self.ChangeDay("left2"))
        homebutton = Button(topframe, text="HOME", command=lambda: self.ChangeDay("home"))

        rightbutton2.pack(side=RIGHT)
        rightbutton.pack(side=RIGHT)
        homebutton.pack(side=RIGHT)
        leftbutton.pack(side=RIGHT)
        leftbutton2.pack(side=RIGHT)
        TagButton.pack(side=RIGHT)

        progressbar = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200,
                                      mode='determinate', maximum=750, variable=self.wordCount)

        self.time_since_opening = StringVar()
        lastTimeDisplay = Label(
            self.mainframe, textvariable=self.time_since_opening, background="grey")
        self.time_since_opening.set("00:00:00")

        dateDisplay.pack(side=TOP, fill=BOTH)

        topframe.pack(side=TOP, fill=BOTH)

        self.text.pack(side=TOP, fill=BOTH, expand=1)
        bottomframe.pack(side=BOTTOM)
        words.pack(side=RIGHT)
        lastTimeDisplay.pack(side=LEFT)
        progressbar.pack(side=LEFT, expand=1, fill=X)

        quitButton.pack(side=LEFT)
        infoButton.pack(side=RIGHT)

        # Put the window on top. Some additional content if mac
        self.root.lift()
        if (sys.platform.startswith("darwin")):
            os.system(
                ''' /usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        # Set bindings:
        # Recount words after each keypress
        self.root.bind('<KeyPress>', self.CountWords)
        # Make a save after every newline
        self.root.bind('<Return>', self.SaveEntry)
        # Bind Alt-arrow to change the day
        self.root.bind('<Mod2-Left>', lambda a: self.ChangeDay("left"))
        self.root.bind('<Mod2-Right>', lambda a: self.ChangeDay("right"))
        self.root.bind('<Mod2-Up>', lambda a: self.ChangeDay("home"))

    def find_dropbox_path(self):

        # Get dropbox's location
        if (sys.platform.startswith("linux")):
            dropbox_config_path = expanduser("~") + "/.dropbox/info.json"
        elif (sys.platform.startswith("darwin")):
            dropbox_config_path = expanduser("~") + "/.dropbox/info.json"
        elif (sys.platform.startswith("win")):
            dropbox_config_path = os.getenv('APPDATA') + "\Dropbox\info.json"
        else:
            print("Failed to get Dropbox's config file path, using local folder")
            self.journal_file_entries = 'entries.txt'
            return None

        print("dropbox_config_path: " + dropbox_config_path)
        try:
            dropbox_config_file = open(dropbox_config_path)
        except:
            print("failed opening Dropbox's config file")

        dropbox_config_content = dropbox_config_file.read()
        dropbox_config_json = json.loads(dropbox_config_content)
        dropbox_folder_path = dropbox_config_json["personal"]["path"]
        print("dropbox_path: " + dropbox_folder_path)
        # journal_file = dropbox_folder_path + '/.journal.txt'
        self.journal_file_entries = dropbox_folder_path + '/.entries.txt'
        # self.journal_file_entries = dropbox_folder_path + '/.entries_test.txt'

        print("saving entries to " + self.journal_file_entries)

    # def set_local_path(self):
    #     """ Set path to current folder """
    #     print("Saving data to local folder")
    #     self.journal_file_entries = "/.entries.txt"

    def load_entries(self):
        # Load all entries
        try:
            myfile_entries = open(self.journal_file_entries)
            jsondump_entries = myfile_entries.read()
            self.my_entries = jsonpickle.decode(jsondump_entries)
            self.dateload(self.currentdate)

        except:
            # Seems that it enters here, not sure why ...
            print("Entries file not found, creating a new file ...")
            self.my_entries = dict()

    def update_time(self):
        """ Update time since program open
        """
        self.last_touch = datetime.now()
        origindate = datetime(2000, 1, 1, 00, 00, 0)

        # Time since last touch
        deltaInit = datetime.now() - self.initTime
        # Update time since beginning
        self.time_since_opening.set((origindate + deltaInit).strftime("%H:%M:%S"))
        self.root.after(1000, self.update_time)

    def retrieve_input(self):
        return self.text.get("1.0", "end-1c")

    def on_closing(self):
        if messagebox.askyesno("Save", "Do you want to save?"):
            self.SaveEntry()
        self.root.destroy()

    def CountWords(self, *args):
        """
        Update when a key is typed
        """

        input_str = self.retrieve_input()
        nwords = len(input_str.split())
        self.wordCount.set(nwords)
        self.wordsText.set(str(nwords) + " words")

    def CountWordsAllEntries(self):
        """ Count all words in all entries"""

        # Intialize Counter
        counts = Counter()

        # Should not be necessary to go all over them. Just do it once ...
        for _, entry in self.my_entries.items():
            counts.update(entry.body.lower().split())

        wordList = []
        for key, value in counts.items():
            wordList.append([value, str(key)])

        wordList.sort(reverse=1, key=lambda x: x[0])
        self.l_word_count.set(tuple(wordList))

    def SaveEntry(self, *args):
        """
        Update when a return is typed. Goal is to save the data here ...
        :param args:
        """

        input_str = self.retrieve_input()
        if input_str != "" or True:  # Not sure yet how to work this out.
            newentry = methods.new_entry(input_str, self.currentdate)
            self.my_entries[str(newentry.date)] = newentry

            print("self.my_entries length (entries): " + str(len(self.my_entries.keys())))

            # For several entries
            jsondump_entries = jsonpickle.encode(self.my_entries)
            myfile_entries = open(self.journal_file_entries, "w")
            myfile_entries.write(jsondump_entries)
            myfile_entries.close()

    def display_info(self):
        """ Display statistics over the words used

        """
        # Probably there is a better way than to create everything here, it should just appear...

        self.CountWordsAllEntries()

        t = Toplevel(self.root)
        t.geometry('300x200+' + str(self.root.winfo_width() + self.root.winfo_x() + 20) + '+' + str(
            self.root.winfo_y()))  # Set it next to the initial window

        lbox = Listbox(t, listvariable=self.l_word_count, height=5)
        lbox.pack(fill=BOTH, expand=1)

    def ChangeDay(self, direction):
        """ Go to a new entry
        """
        max_days_search = 20
        # Save the text
        self.SaveEntry()
        if direction == "right":
            self.currentdate = self.currentdate + timedelta(days=1)
        elif direction == "left":
            self.currentdate = self.currentdate + timedelta(days=-1)
        # Move 20 days max, or to previous day
        elif direction == "left2":
            for days_ in range(1, max_days_search):
                day = self.currentdate - timedelta(days=days_)
                print(str(day))
                if str(day) in self.my_entries:
                    print(self.my_entries[str(day)].body)
                if str(day) in self.my_entries and self.my_entries[str(day)].body != "":
                    break
            self.currentdate = day

        elif direction == "right2":
            for days_ in range(1, max_days_search):
                day = self.currentdate + timedelta(days=days_)
                if str(day) in self.my_entries and self.my_entries[str(day)].body != "":
                    break
            self.currentdate = day

        else:
            self.currentdate = date.today()

        self.dateload(self.currentdate)

    def dateload(self, date):
        """ Load desired date

        """
        self.text.delete(1.0, END)
        if (str(date) in self.my_entries):
            self.text.insert(1.0, self.my_entries[str(date)].body)
        else:
            self.text.insert(1.0, "")
        # Set new date on top ...
        self.dateDisplayText.set(self.currentdate.strftime("%A %d %b %Y"))

        # Change position of the cursor to end of file.
        self.text.mark_set(INSERT, END)
        # Scroll to desired position
        self.text.see(INSERT)
        # Set focus on the self.text area (ready to write)
        self.text.focus_set()

        # Update number of words
        self.CountWords()

    def insertTime(self):
        """ Insert current time into the text.

        Different behaviour depending on current line's content
        """
        stringtemp = "--- TIME: " + datetime.today().strftime("%H:%M") + "---"

        if (self.text.get("insert linestart", "insert lineend").strip() == ""):
            print("empty line")
        else:
            print("There is something on the line")

        stringtemp += "\n"

        self.text.insert("insert linestart", stringtemp)


def main():
    Journal()


if __name__ == '__main__':
    main()
