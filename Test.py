# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog
from tkinter import messagebox

import cv2
import os
import numpy as np
import math

#check = 1
# Function for opening the
# file explorer window
def browseFiles():
    global check
    global filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select Video",
                                          filetypes = (("avi files",
                                                        "*.avi*"),
                                                        ("all files",
                                                        "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)
    check = int(os.path.isdir(os.path.dirname(filename)+ '\Patient'))
    if(check == 1):
        messagebox.showerror("Error", "One set of images already exist; remove the directory and try again")



def slicing():

    cap = cv2.VideoCapture(filename)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if(int(frame.get())>1 and int(frame.get())<frameCount and check == 0 ):

        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
        fc = 0
        ret = True

        while (fc < frameCount  and ret):
            ret, buf[fc] = cap.read()
            fc += 1

        cap.release()

        frames = buf.shape[0]
        #image_to_extract = int(input('How many images do you want to extract from video? :'))

        image_to_extract = int(frame.get())
        NEW_DIR = os.path.dirname(filename)+ '\Patient'
        new_dir_path = NEW_DIR
        os.mkdir(new_dir_path)

        fc = 0
        ret = True

        j = 1
        step = math.trunc(frames/image_to_extract)
        for i in range(0, frames, step):
            cv2.imwrite(os.path.join(new_dir_path, 'Paz_Task_%d.tiff' % j), buf[i,:,:])
            j = j + 1
            if j == image_to_extract+1: break
    elif(check == 1):
        messagebox.showerror("Error", "One set of images already exist; remove the directory and try again")
    else:
        messagebox.showerror("Error", "Incorrect n° of slice")

# Create the root window
window = Tk()

# Set window title
window.title('Video Slicer')

windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)

# Positions the window in the center of the page.
window.geometry("+{}+{}".format(positionRight, positionDown))

#Set window background color
window.config(background = "#D1F2EB")

# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "Video Slicer",
                            width = 100, height = 4,
                            background = "#D1F2EB",
                            fg = "#154360")

button_explore = Button(window,
                        text = "Browse Files",
                        background = "#48C9B0",
                        command = browseFiles)

label_slice = Label(window,
                    text = "Select n° of frames:",
                    background = "#D1F2EB",
                    fg = "#154360").grid(row = 3)

frame = Entry(window)

button_slice = Button(window,
                     text = "Start Slice",
                     background = "#48C9B0",
                     command = slicing )

button_exit = Button(window,
                     text = "Exit",
                     background = "#48C9B0",
                     command = exit )

style_label = Label(window,
                    text = "   ",
                    width = 100, height = 4,
                    background = "#D1F2EB")

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)

button_explore.grid(column = 1, row = 2)

#label_slice.grid(column = 1, row = 3)

frame.grid(column = 1,row = 3)

button_slice.grid(column = 1,row = 4)

button_exit.grid(column = 1,row = 5)

style_label.grid(column = 1, row = 6)


# Let the window wait for any events
window.mainloop()
