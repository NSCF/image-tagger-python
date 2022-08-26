import os

index = 120
size = 5

image_dir = r'G:\PRE'
fileext = '.tif'
images = os.listdir(image_dir)
images = list(filter(lambda x: x.endswith(fileext), images))
slice = images[index : index + size]