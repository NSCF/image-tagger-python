# resizes all jpegs in a directory by a certain proportion (e.g. half) and places them in a subdirectory called 'small'.
# note this will not check subdirectories

import os, time, math
import concurrent.futures
from PIL import Image
from progress.bar import Bar


dir = r"E:\Herbarium images\Quick Guide" # the directory to read
prop = 0.90 # The proportional reduction 

### SCRIPT ####

if prop >= 1.0:
  print('Proportion must be less than 1')
  exit()

jpegs = set()

print('reading directory...')
for file in os.listdir(dir):
  if file.lower().endswith(('.jpg', '.jpeg')):
    jpegs.add(file)

if len(jpegs) == 0:
  print('no jpeg files in this directory')
  exit()

dest_dir = os.path.join(dir, 'small')
if not os.path.exists(dest_dir):
  os.makedirs(os.path.join(dest_dir))

# there may already be some images generated, and we want to skip those
existing = set()
for file in os.listdir(dest_dir):
  if file.lower().endswith(('.jpg', '.jpeg')):
    existing.add(file)

jpegs = jpegs - existing
if len(jpegs) == 0:
  print('All files have already been converted')
  exit()

def process_image(jpeg, dir, dest_dir, prop, bar):
  img = Image.open(os.path.join(dir, jpeg))
  width, height = img.size
  resized = img.resize((int(width * prop), int(height * prop)), Image.Resampling.LANCZOS)
  resized.save(os.path.join(dest_dir, jpeg))
  bar.next()

start = time.time()
bar = Bar('Processing', max = len(jpegs))
print('resizing images...')

prop = 1 - prop # because 95 % reduction means 5% the original size...
prop = math.sqrt(prop)
counter = 0

bar.finish()

# thanks ChatGPT...
with concurrent.futures.ThreadPoolExecutor() as executor:
  # Submit tasks to the executor
  futures = [executor.submit(process_image, jpeg, dir, dest_dir, prop, bar) for jpeg in jpegs]
  
  # Wait for all futures to complete
  for future in concurrent.futures.as_completed(futures):
    try:
      future.result()  # Check for exceptions
    except Exception as e:
      print(f"Error processing file: {e}")

end = time.time()
duration = end - start
hours, rem = divmod(duration, 3600)
minutes, seconds = divmod(rem, 60)
print('Images resizing completed in', f"{round(hours):02}:{round(minutes):02}:{round(seconds):02}")

print('all done...')










