from PIL import Image
import piexif
import pandas as pd
import os 
from os import listdir

#read in images from directory
image_dir = "C:\DevProjects\ImageTagging\TaggingProject_Images"
for images in os.listdir(image_dir):
    if (images.endswith)(".jpg"):
        print(images)

#read csv as dataframe
df = pd.read_csv("Keywords.csv")
print(df)

#try first add tags to single image
file = "BOL0044784.jpg"
exif_dict = piexif.load(file)
#print(exif_dict)
keywords = "; ".join([df.loc[0][1], df.loc[0][2], df.loc[0][11]])
exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le") 
piexif.insert(piexif.dump(exif_dict), file)