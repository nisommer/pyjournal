__author__ = 'nicolassommer'

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")

        self.entry = tk.Entry(self)
        self.entry["text"] = "entry"
        self.entry.pack(side="bottom")

        self.display = tk.Text(self)
        self.display.pack(side="bottom")

    def say_hi(self):
        self.hi_there["text"]= "(" +self.hi_there["text"] + self.entry.get()

root = tk.Tk()
app = Application(master=root)
app.mainloop()