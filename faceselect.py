'''
TkInter GUI app to go through cropped faces and keep/remove each one.
'''

import os
import copy
from tkinter import Tk, Canvas, messagebox
from PIL import Image, ImageTk

from common import list_files

class MainWindow():
    '''
    Main GUI window
    
    Attributes
    ----------
    img_number : int
        Index of the currently shown image
    prev_img : bytearray
        Previous image for undo if it has been removed
    prev_img_path : str
        Path of the previously deleted image for undo 
    num_images : int
        Number of images in training-cropped dir
    canvas : tkinter.Canvas
        Canvas for photos
    canvas_img : int
        ID number of the image object on self.canvas
    '''

    def __init__(self, main):
        '''
        Initialize GUI and class variables

        Parameters
        ----------
        main : tkinter.Tk
            Main Tk app
        '''

        self.img_number = 0
        self.prev_img = None
        self.prev_img_path = None
        self.num_images = len(imgs)

        self.canvas = Canvas(main, width=800, height=800)
        self.canvas.grid(row=0, column=0)
        
        self.load_image(imgs[0])
        self.canvas_img = self.canvas.create_image(400, 400, anchor='center', image=self.img)

    def keypress(self, event):
        '''
        Capture arrow keypress and remove, undo or continue with next image

        Parameters
        ----------
        event : tkinter.Event
            Keypress event containing e.g. the pressed key
        '''

        if event.keysym == "Left":
            with open(imgs[self.img_number], 'rb') as f:
                self.prev_img = f.read()
            self.prev_img_path = imgs[self.img_number]
            os.remove(imgs[self.img_number])

        elif event.keysym == 'Down':
            if self.prev_img:
                with open(self.prev_img_path, 'wb') as f:
                    f.write(self.prev_img)
                self.prev_img = None
                self.prev_img_path = None
                self.img_number -= 2
            elif self.img_number > 0:
                self.img_number -= 2
            else:
                messagebox.showerror('Notice', 'Only 1 level of undo available')
                return

        if self.img_number == (self.num_images - 1):
            messagebox.showinfo('Notice', 'All images checked')
            return

        self.img_number += 1
        self.load_image(imgs[self.img_number])
        self.canvas.itemconfig(self.canvas_img, image=self.img)
    
    def load_image(self, imgpath):
        '''
        Load image from given path to self.img as ImageTk.PhotoImage

        Parameters
        ----------
        imgpath : str
            Full path to the image to be loaded
        '''
    
        im = Image.open(imgpath)
        im.thumbnail((800,800), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(im)

if __name__ == '__main__':
    crop_path = os.path.join('img', 'training-cropped')
    imgs = list_files(crop_path)
    main = Tk()
    mw = MainWindow(main)
    main.title('Left = remove   Down = undo   Right = Keep')
    main.bind('<Left>', mw.keypress)
    main.bind('<Right>', mw.keypress)
    main.bind('<Down>', mw.keypress)
    main.mainloop()