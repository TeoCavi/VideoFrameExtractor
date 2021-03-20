from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
import os
import shutil
import numpy as np


def BrowseDataset():
    global dataset_dir
    dataset_dir = filedialog.askdirectory()


def DirectoryCreation():
    global check
    global new_patient
    global filename
    filetype = (("avi files", "*.avi"), ("all files", "*.*"))
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select Video",
                                          filetypes = filetype )

    full_name = os.path.basename(filename)
    print(full_name)
    name = os.path.splitext(os.path.basename(filename))[0]
    fname = name.split("_")

    pid = str(fname[0])
    task = fname[1]
    video_num = str(fname[2])

    label_file_explorer.configure(text="Patient n°: "+pid)

    patients = next(os.walk(dataset_dir))[1]

    new_patient = 1
    for patient in patients:
        if (patient == f"Patient_{pid}"):
            new_patient = 0

    first_level_dir = ["Video","Images","Segmentations"]
    patient_dir = os.path.join(dataset_dir, f"Patient_{pid}")
    video_folder = os.path.join(patient_dir, first_level_dir[0])
    image_folder = os.path.join(patient_dir, first_level_dir[1])
    video_folder_task = os.path.join(patient_dir, first_level_dir[0], task)
    image_folder_task = os.path.join(patient_dir, first_level_dir[1], task)
    segmentation_folder_task = os.path.join(patient_dir, first_level_dir[2], task)

    if new_patient == 1: #nuovo paziente nel database
        case = "NewPatient"
        os.mkdir(patient_dir)

        for dir in first_level_dir:
            os.mkdir(os.path.join(patient_dir, dir))

        os.mkdir(video_folder_task)
        os.mkdir(image_folder_task)
        os.mkdir(segmentation_folder_task)
        shutil.copy(filename, video_folder_task)

        messagebox.showerror("Error", case)

    if new_patient == 0: #paziente già inserito
        tasks = next(os.walk(video_folder))[1] #[1] --> detects directories

        for t in tasks:
            if t == task:
                videos = next(os.walk(video_folder_task))[2] #[2]--> detects files

                case = "NewVideoSameTask"
                for v in videos:
                    if v == full_name:
                        case = "ChangeNumFrame"

                if(case == "ChangeNumFrame"):
                    messagebox.showerror("Error", case)
                if(case == "NewVideoSameTask"):
                    shutil.copy(filename, video_folder_task)
                    messagebox.showerror("Error", case)


            else:
                case = "NewVideoDiffTask"
                os.mkdir(video_folder_task)
                os.mkdir(image_folder_task)
                os.mkdir(segmentation_folder_task)
                shutil.copy(filename, video_folder_task)
                messagebox.showerror("Error", case)















def slicing():

    cap = cv2.VideoCapture(os.path.join(video_folder,full_name))
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
        image_to_extract = int(frame.get())

        fc = 0
        ret = True

        step = int(frames/image_to_extract)
        for i in range(0, frames, step):
            cv2.imwrite(os.path.join(image_folder, f"p{pid}_t{task}_n{video_num}_f{i}"), buf[i,:,:])
            if i >= image_to_extract: break
    elif(check == 1):
        messagebox.showerror("Error", "One set of images already exist; remove the directory and try again")
    else:
        messagebox.showerror("Error", "Incorrect n° of slice")










    check = int(os.path.isdir(os.path.dirname(filename)+ '\Patient'))
    if(check == 1):
        messagebox.showerror("Error", "One set of images already exist; remove the directory and try again")









window = Tk()
window.title('Video Slicer')
#window.geometry("500x500")
window.grid_columnconfigure(5, minsize=100)
window.grid_rowconfigure(5, minsize=100)





label_file_explorer = Label(window,
                            text = "Video Slicer",
                            width = 100, height = 4,
                            fg = "#154360")

button_explore_dataset = Button(window,
                        text = "Browse Dataset",
                        background = "#48C9B0",
                        command = BrowseDataset)

button_explore_video = Button(window,
                        text = "Browse Video",
                        background = "#48C9B0",
                        command = DirectoryCreation)



label_file_explorer.grid(column = 2, row = 1)

button_explore_dataset.grid(column = 2, row= 2)

button_explore_video.grid(column = 2, row = 3)

window.mainloop()








#parent = 'C:\\Users\matte\Google Drive\Segmentazione PoliMi'
#folder = 'Dataset'
#os.mkdir(os.path.join(parent, folder))
