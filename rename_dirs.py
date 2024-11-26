# for renaming directories holding specimen images that have not been named corrected

import os
import re

dir = r'E:\Type specimen imaging\Evolutionary Studies Institute\ESI Karoo Vertebrates\RAW'

contents = os.listdir(dir)
directories = [entry for entry in contents if os.path.isdir(os.path.join(dir, entry))]
i = 0

counter = 0
for directory in directories:
  if directory.startswith('BP-'):
    new_name = directory.replace('BP-', 'BP1-')
    os.rename(os.path.join(dir, directory), os.path.join(dir, new_name))
    counter += 1

print('updated', counter, 'directory names')