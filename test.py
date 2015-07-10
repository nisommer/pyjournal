__author__ = 'nicolassommer'

from tkinter import *
from tkinter import ttk
root = Tk()



b={'a': 1,'b':2,'c':3}


list2 = []
list3 = ()
list4=set()


for key, value in b.items():
    temp=[key,value]
    list2.append((str(key) + ": " + str(value)))
    list4.add((str(key) + ": " + str(value)))


#list3 = tuple(b.items())
print(list4)
print(list2)
list3 = tuple(list4)
print(list3)
print(tuple(list2))

var = StringVar(value=list3)


lbox = Listbox(root, listvariable=var, height=5)
lbox.pack()

root.mainloop()