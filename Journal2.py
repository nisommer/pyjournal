__author__ = 'nicolassommer'

from tkinter import *
from tkinter import ttk

from collections import Counter # To count each word ...


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

def calculate(*args):
    #print("feet.get2(): " + retrieve_input())

    input_str = retrieve_input()

    ## Count each word separately (do that later ..°
    #print("There are: " + str(Counter(input_str.split())) + "words")

    nwords = len(input_str.split())
    wordCount.set(nwords)
    wordsText.set(str(nwords) + " words")



root = Tk()
root.title("Journal test program")


mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

text = Text(mainframe)

quitButton = Button(mainframe, text="QUIT", command=root.destroy)

wordCount = IntVar() # Number of words
wordsText = StringVar() # Contents of the text widget

words = Label(mainframe,textvariable=wordsText,background="grey")
wordsText.set("0 words")

progressbar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=200, mode='determinate', maximum = 750, variable=wordCount)

text.grid(column=0, row=0, columnspan = 4)
words.grid(column=3, columnspan = 1, row=1 )
quitButton.grid(column=0, row = 2, columnspan=4)
progressbar.grid(column = 0, row=1, sticky=(W, E)) # Pas clair comment répartir les elements sur la grille !







# Set padding
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)


# Set bindings
root.bind('<KeyPress>', calculate)

# Run the program
root.mainloop()