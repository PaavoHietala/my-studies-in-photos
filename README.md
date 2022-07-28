# my-studies-in-photos

Crawl the online galleries of student associations and download all images of yourself.

This repository walks you through creating a training set, training the model, crawling the galleries and selecting/saving only the images which include your face.

## Usage

### Preparations

1. Clone this repository to your computer
2. Install required libraries with `python -m pip install -r requirements.txt`
3. Run `python prepare.py -n` to set up the correct directory structure inside the project

### Crop faces for model training

To teach the model to detect your face you need to first create a training set from existing photos.
This can be achieved with `facecrop.py`:

1. Place a number (100+) images of yourself in `img\training-full`
2. Run `python facecrop.py`
3. Check the results in `img\training-cropped` for cropped faces and `img\training-detected` for original images marked with detected faces
4. If you need to tweak the detection it can be done in `facecrop.py` (currently the parameters are hardcoded). Most useful tweaks are to change the cascade type on the last line and the number of neighbors in `cascade.detectMultiScale(img, 1.1, 2)`. Before trying again you can clean up the output directories with `python prepare.py -c`

### Prune the cropped faces

The `facecrop.py` is very likely to detect faces of other people or irrelevant features in the background. To remove all unnecessary images from the `img\training-cropped` folder, a GUI app is provided.

1. Run pruning app with `python faceselect.py`
2. Press right arrow key to keep the image (you are in the image)
3. Press left arrow to delete image
4. Press down arrow to undo last action (undo stack has max. 1 item)
5. You will get a notification once the last image has been refereed

## TODO

1. ~~App to browse through cropped faces and confirm/discard a face as yours~~  
2. "Am I in this image?" Face matching based on cropped faces training set
3. Crawler for kuvat.fi
4. Crawler for flickr.com
