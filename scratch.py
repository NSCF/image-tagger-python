import piexif

#file = 'C:/Users/engelbrechti/Desktop/temp/Uro ZamF.JPG'
file = 'TaggingProject_Images/BOL0044784.jpg'
exif_dict = piexif.load(file)


for ifd_name in exif_dict:
    if ifd_name == 'thumbnail':
      continue
    print("\n{0} IFD:".format(ifd_name))
    for key in exif_dict[ifd_name]:
        keyname = piexif.TAGS[ifd_name][key]['name']
        keytype = piexif.TAGS[ifd_name][key]['type']
        val = exif_dict[ifd_name][key]
        try:
            if keytype == 2: #string, but we need to decode
              print(keyname +':', exif_dict[ifd_name][key].decode())
            elif keytype == 5: #rational number
              val = exif_dict[ifd_name][key][0] / exif_dict[ifd_name][key][1]
              print(keyname +':', val)
            else:
              print(keyname +':', exif_dict[ifd_name][key])
        except:
            print(keyname, exif_dict[ifd_name][key])
