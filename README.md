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

Edit the file `journal` as follows
```
#!/bin/sh
python /PATH_TO_FOLDER/Journal_new.py
```

