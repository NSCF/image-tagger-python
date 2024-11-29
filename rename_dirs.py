# for renaming directories holding specimen images that have not been named corrected

import os
import re

dir = r'D:\Type specimen imaging\Evolutionary Studies Institute\ESI Karoo Vertebrates\RAW'
find = r"BP1_" # what to replace, can also just be a something like "BP_" as long as there are no characters that mean anything in regex
replace = "BP1-" #this is just a plain string

contents = os.listdir(dir)
directories = [entry for entry in contents if os.path.isdir(os.path.join(dir, entry))]

counter = 0
for directory in directories:
  new_name = re.sub(find, replace, directory)
  if directory != new_name:
    os.rename(os.path.join(dir, directory), os.path.join(dir, new_name))
    counter += 1

print('updated', counter, 'directory names')