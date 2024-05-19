## Tagging images with values from a dataset

A basic Python script to add a series of keywords from a dataset to a corresponding set of specimen images, as well as copyright and license tags. Expects the filename of the image (with file extension removed) to match a unique value, such as catalog number or barcode, in the dataset provided. 

Uses the excellent ExifTool ([exiftool.org](https://exiftool.org/)) to do the tagging. Make sure that ExifTool is installed first and available on your PATH.

Before running any scripts make sure to run `pip install -r requirements.txt`.

Open ImageTagger.py, change the values in the SETTINGS section at the top of the file to represent what you want. Make sure that the fields you list in `keywordfields` are present in your dataset. Save and run the script in a terminal with `python ImageTagger.py`

Please add comments, suggestions, and issues in the Issues section here in Github.

Currently under active development and testing.
