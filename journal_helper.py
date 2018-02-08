import re
# from __future__ import absolute_import, unicode_literals
import Entry
# import time # does not seem to be working

__author__ = 'Nico'

from datetime import date, timedelta


# class Entry:
#     def __init__(self, date=date.today(), title="", body="", starred=False):
#         # self.journal = journal  # Reference to journal mainly to access it's config
#         # self.date = date or datetime.now()
#         self.date = date or date.today()
#         self.title = title.rstrip("\n ")
#         self.body = body.rstrip("\n ")
#         # self.tags = self.parse_tags()
#         # self.starred = starred
#         self.modified = False
#         # print(" init title: " + title)
#         # print(" init body: " + body)


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
        body = raw

    starred = False

    if not date:  # Still nothing? Meh, just live in the moment.
        date = date.today

    entry = Entry.Entry(date, title, body, starred=starred)
    entry.modified = True

    # if sort:
    #    self.sort()
    return entry
