# pyjournal
My take on a simple python journal. 
The goal is to easily write something everyday.
No documentation yet and a lot to clean but works already quite well.

Based on *tkinter* to generate the graphic interface

# Some guidance
- Requires python3+
- Requires the python library jsonpickle (`pip install jsonpickle`)

For daily usage, it's recommended to run it with a shortcut.
# Example shortcut for mac/linux:

- Create shortcut and edit
```
cd DESIRED_PATH_TO_SHORTCUT
nano journal
chmod 755 journal
```

Edit the file `journal` as follows:
```
#!/bin/sh
python /PATH_TO_FOLDER/pyjournal.py
```

# Shortcuts
- Go to Next/Prev/Current Day  -->  Alt + Right/Left/Up

# How is the data saved ?
If Dropbox is installed, entries are automatically saved as a hidden file ".entries_s.txt" at the root of the Dropbox folder. This allows seemless sync between computers.
Otherwise, entries are saved in the same folder as the code (not hidden).
Entries are saved with jsonpickle as simple dictionnaries ({date: text}). This makes them easy to read without this software.
