import re
from datetime import datetime
#from __future__ import absolute_import, unicode_literals
#import Entry
#import time # does not seem to be working

__author__ = 'Nico'
import Entry


def new_entry(raw, date=None, sort=True):
        """Constructs a new entry from some raw text input.
        If a date is given, it will parse and use this, otherwise scan for a date in the input first."""

        raw = raw.replace('\\n ', '\n').replace('\\n', '\n')
        starred = False
        # Split raw text into title and body
        sep = re.search("\n|[\?!.]+ +\n?", raw)
        title, body = (raw[:sep.end()], raw[sep.end():]) if sep else (raw, "")

        # Overwrite this result:
        if 1:
            title = ""
            body=raw

        print("title: " + title)
        print("body: " + body)


        ## Title parsing is not good : do it manually : take the first line ! or just dont take titles ...
        starred = False
        if not date:
            if title.find(": ") > 0:
                starred = "*" in title[:title.find(": ")]
                #date = time.parse(title[:title.find(": ")], default_hour=self.config['default_hour'], default_minute=self.config['default_minute'])
                if date or starred:  # Parsed successfully, strip that from the raw text
                    title = title[title.find(": ")+1:].strip()
            elif title.strip().startswith("*"):
                starred = True
                title = title[1:].strip()
            elif title.strip().endswith("*"):
                starred = True
                title = title[:-1].strip()
        if not date:  # Still nothing? Meh, just live in the moment.
            #date = time.parse("now")
            date = datetime.now()# This should be changed

        entry = Entry.Entry( date, title, body, starred=starred)
        entry.modified = True

        #self.entries.append(entry)
       # if sort:
        #    self.sort()
        return entry
