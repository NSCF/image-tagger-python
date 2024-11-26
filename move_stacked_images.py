# move stacked images from inside specimen folders to a single tiff folder

import os
import shutil

target_dir = r'D:\Type specimen imaging\Evolutionary Studies Institute\ESI Karoo Vertebrates\RAW'
dest_dir = r'D:\Type specimen imaging\Evolutionary Studies Institute\ESI Karoo Vertebrates\TIFF'

dirs = [entry for entry in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, entry))]

no_stacked = []
moved = 0
print('moving files...')
for dir in dirs:
  contents = os.listdir(os.path.join(target_dir, dir))
  stacked_dir = next((x for x in contents if 'stack' in x.lower()), None)
  if stacked_dir:
    stacked_images = os.listdir(os.path.join(target_dir, dir, stacked_dir))
    if len(stacked_images):
      for image in stacked_images:
        shutil.move(os.path.join(target_dir, dir, stacked_dir, image), dest_dir)
        moved += 1
    else:
      no_stacked.append(dir)
  else:
    no_stacked.append(dir)

print('moved', moved, 'files')

if len(no_stacked):
  print('The following directories have no stacked images:')
  for item in no_stacked:
    print(item)

print('all done!')

