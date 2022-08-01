from PIL import Image
import piexif
import pandas as pd
import os 
from os import listdir
import numpy as np

#read in images from directory
#image_dir = "C:\DevProjects\ImageTagging\TaggingProject_Images"
#for images in os.listdir(image_dir):
#    if (images.endswith)(".jpg"):
#        print(images)

#read csv as dataframe
df = pd.read_csv("Keywords.csv")
print(df)

for dirname, dirnames, filenames in os.walk('TaggingProject_Images'):
#    print(filenames)
    for filename in filenames:
       if filename.endswith('.jpg'):
            nam = df['Barcode']
            for ind, x in enumerate(nam):
                if x + ".jpg" == filename:
                    filepath = dirname + "/" + filename
                    exif_dict = piexif.load(filepath)
                    for ifd_name in exif_dict:
                        print("\n{0} IFD:".format(ifd_name))
                        for key in exif_dict[ifd_name]:
                            try:
                                print(key, exif_dict[ifd_name][key][:10])
                            except:
                                print(key, exif_dict[ifd_name][key])

                    #print(exif_dict)
                    keywords = "; ".join([df.loc[ind][2]])
                    exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le") 
                    piexif.insert(piexif.dump(exif_dict), filepath)

#for line in df:
#    nam = df['Barcode']
#    print(nam)


#    print(x)
#print(nam)


#try first add tags to single image
filename = "BOL0044784.jpg"
exif_dict = piexif.load(file)
#print(exif_dict)
keywords = "; ".join([df.loc[0][1], df.loc[0][5], df.loc[0][6], df.loc[0][11], df.loc[0][12]])
exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le") 
piexif.insert(piexif.dump(exif_dict), file)