'''
Crop all faces from images in img\\training-full and save them in img\\training-crop.
'''

import os
import copy

import cv2
import numpy as np
import matplotlib.pyplot as plt

from common import list_files

def read_gray(fpath, debug = False):
    '''
    Read the image file in given path and return it in grayscale

    Parameters
    ----------
    fpath : str
        Full path to the image file
    debug : bool, optional
        Draw loaded image before continuing, by default False

    Returns
    -------
    np.array
        Loaded grayscale image array
    '''

    print("Reading file", fpath)

    img = cv2.imdecode(np.fromfile(fpath, np.uint8), cv2.IMREAD_UNCHANGED)

    if img is None:
        print("Loading image failed")
        return None
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if debug:
            plt.imshow(gray, cmap = 'gray')
            plt.show()
        return gray

def crop_faces(img, cascade, fname, suffix = None, debug = False):
    '''
    Detect all faces from the image and save each as a cropped image file.

    Parameters
    ----------
    img : np.array
        Image array for detection
    cascade : cv2.CascadeClassifier
        Preloaded classifier object used for face detection
    fname : str
        Name of the image file without path
    suffix : str
        Suffix to append to filename, e.g. cascade type, by default None
    debug : int, optional
        Debug level 1 (Draw image with detection squares) or 2 (Draw individual
        faces and image with detection squares), by default False
    '''

    pd = 25 # padding for the detecttion square
    det_img = copy.deepcopy(img)
    faces = cascade.detectMultiScale(img, 1.1, 2)
    
    try:
        print("Detected", faces.shape[0], "face(s) in", fname)
    except AttributeError as e:
        print("No faces detected in", fname)
        print(e)
        return

    for i, (x, y, w, h)  in enumerate(faces):
        cv2.rectangle(det_img, (x - pd, y - pd), (x + w + pd, y + h + pd), (0, 0, 255), 2)

        face = img[y - pd : y + h + pd, x - pd : x + w + pd]
        
        if debug == 2:
            cv2.imshow("Face " + str(i), face)
            cv2.waitKey()

        face_name = '-'.join(filter(None, [fname, suffix, str(i)])) + '.jpg'
        face_path = os.path.join('img', 'training-cropped', face_name)
        print("Writing face to path", face_path)

        try:
            _, face = cv2.imencode('.jpg', face)
            face.tofile(face_path)
        except cv2.error as e:
            print("Failed to save face due to error:", e)

    detected_name = '-'.join(filter(None, [fname, suffix, 'detected.jpg']))
    cv2.imwrite(os.path.join('img', 'training-detected', detected_name), det_img)
    
    if debug:
        cv2.imshow('Detected faces', img)
        cv2.waitKey()

if __name__ == "__main__":
    training_dir = os.path.join('img', 'training-full')

    front_cascade = cv2.CascadeClassifier(os.path.join('resources', 'haarcascade_frontalface_alt2.xml'))
    profile_cascade = cv2.CascadeClassifier(os.path.join('resources', 'haarcascade_profileface.xml'))
    lbp_cascade = cv2.CascadeClassifier(os.path.join('resources', 'lbpcascade_frontalface_improved.xml'))

    for fpath in list_files(training_dir):
        img = read_gray(fpath)
        if img is not None:
            crop_faces(img, front_cascade, os.path.split(fpath)[-1], 'front')


  






