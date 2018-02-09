# !/usr/bin/env python
import jsonpickle

# Convert old format entries file to new format (no class definition, easier to change)

# hardcoded here so less things to load
dropbox_folder_path = "/Users/nicolassommer/Dropbox/"
journal_file_entries = dropbox_folder_path + '/.entries.txt'

myfile_entries = open(journal_file_entries)
jsondump_entries = myfile_entries.read()
my_entries = jsonpickle.decode(jsondump_entries)

print(my_entries)
my_entries_string = {key: value.body for key, value in my_entries.items()}

print(my_entries_string)


jsondump_entries_s = jsonpickle.encode(my_entries_string)
myfile_entries = open(dropbox_folder_path + ".entries_s.txt", "w")
myfile_entries.write(jsondump_entries_s)
myfile_entries.close()
