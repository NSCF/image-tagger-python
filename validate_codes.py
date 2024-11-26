# validate that codes are correct for a set of images before tagging
import os, re
from view_codes import make_view

image_dir = r''
fileext = '.tif'

print('reading image directory')
try:
  images = os.listdir(image_dir)
except Exception as ex:
  print('Oops! ' + str(ex))
  exit()

images = list(filter(lambda x: x.lower().endswith(fileext.lower()), images))
code_errors = set()
for image in images:
  parts = re.split(r"[_\.]", image)
  parts.pop() #drop the file extension
  parts = parts[1:] # drop the catalog number
  for part in parts:
    try:
      make_view(part)
    except:
      code_errors.add(image)

if len(images):
  print('The following images have view code errors:')
  for image in images:
    print(image)
else:
  print('All image view codes are valid')

print('All done, you can proceed to tagging...')


