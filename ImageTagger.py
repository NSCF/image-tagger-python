import piexif
import pandas as pd
import os 
from os import listdir

##read csv as dataframe
df = pd.read_csv("Keywords.csv")
#print(df)

##read in images from directory
image_dir = "C:\DevProjects\ImageTagging\TaggingProject_Images"
#for images in os.listdir(image_dir):
    #if (images.endswith)(".jpg"):
        #print(images)

##try first add tags to single image
#file = "BOL0044784.jpg"
#exif_dict = piexif.load(file)
#print(exif_dict)
#keywords = "; ".join([df.loc[0][1], df.loc[0][2], df.loc[0][11]])
#exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le") 
#piexif.insert(piexif.dump(exif_dict), file)

##iterate through dataframe 
#for index, row in df.iterrows():
    #print(row[0])

##list filenames in directory
#for filename in os.listdir(image_dir):
    #print(filename)
    
##try tagging multiple images with same info
#for images in os.listdir(image_dir):
    #if (images.endswith)(".jpg"):
        #print(images)
        #exif_dict = piexif.load(images)
        #print(exif_dict)
        #keywords = "; ".join([df.loc[0][1], df.loc[0][2], df.loc[0][11]])
        #exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le") 
        #piexif.insert(piexif.dump(exif_dict), images)

#tag multiple images with unique keywords
for images in os.listdir(image_dir):
    if (images.endswith)(".jpg"):
        #print(images)
        exif_dict = piexif.load(images)
        #print(exif_dict)
    for index, row in df.iterrows():
        keywords = "; ".join([df.loc[index][1], df.loc[index][2], df.loc[index][11]])
        #print(keywords)
    exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le") 
    piexif.insert(piexif.dump(exif_dict), images)
