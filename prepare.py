import pathlib
import os
import sys
import shutil

dir_list = [os.path.join('img', 'training-full'),
            os.path.join('img', 'training-cropped'),
            os.path.join('img', 'training-detected')]

protected = [os.path.join('img', 'training-full')]

fpath = os.path.dirname(os.path.realpath(__file__))

if sys.argv[1] == "-n":
    for dir in dir_list:
        print("Creating dir", os.path.join(fpath, dir))
        pathlib.Path(os.path.join(fpath, dir)).mkdir(parents = True, exist_ok = True)

elif sys.argv[1] in ["-c", "clean"]:
    for dir in [x for x in dir_list if x not in protected]:
        print("Cleaning dir ", os.path.join(fpath, dir))
        shutil.rmtree(os.path.join(fpath, dir))
        os.mkdir(os.path.join(fpath, dir))