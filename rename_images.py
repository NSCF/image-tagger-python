# rename files that used underscores instead of dashes in the catalog number
import os

image_dir = r'E:\ESI Finals Folders\Finals checked.TiffPsd'
find = 'BP1_'
replace_with = 'BP1-'

images = [entry for entry in os.listdir(image_dir) if entry.endswith('.tif') and entry.startswith(find)]

print('renaming images')
counter = 0
errors = []
for image in images:
  new_name = image.replace(find, replace_with)
  try:
    os.rename(os.path.join(image_dir, image), os.path.join(image_dir, new_name))
    counter += 1
  except:
    errors.append(image)

print('renamed', counter, 'images')
if len(errors):
  print('the following file names had errors, possibly they exist already:')
  for err in errors:
    print(err)
print('all done...')
