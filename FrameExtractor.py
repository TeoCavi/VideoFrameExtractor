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
    global cap, frameCount
    global image_folder_task
    global pid, task, video_num

    filetype = (("avi files", "*.avi"), ("all files", "*.*"))
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select Video",
                                          filetypes = filetype )

    full_name = os.path.basename(filename)

    name = os.path.splitext(os.path.basename(filename))[0]
    fname = name.split("_")

    pid = str(fname[0])
    task = fname[1]
    video_num = str(fname[2])

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

    if new_patient == 0: #paziente già inserito
        tasks = next(os.walk(video_folder))[1] #[1] --> detects directories

        case = "NewVideoDiffTask"
        for t in tasks:
            if t == task:
                videos = next(os.walk(video_folder_task))[2] #[2]--> detects files

                case = "NewVideoSameTask"
                for v in videos:
                    if v == full_name:
                        case = "ChangeNumFrame"

                if(case == "NewVideoSameTask"):
                    shutil.copy(filename, video_folder_task)

        if (case == "NewVideoDiffTask"):
            os.mkdir(video_folder_task)
            os.mkdir(image_folder_task)
            os.mkdir(segmentation_folder_task)
            shutil.copy(filename, video_folder_task)

    cap = cv2.VideoCapture(os.path.join(video_folder_task,full_name))
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    label_file_explorer.configure(text=f"Patient n°: {pid}\n N° of frames: {frameCount}\n Case: {case}  ",
                                  width = 100, height = 6)



def slicing():

    if(int(frame.get())>1 and int(frame.get())<frameCount):

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
        j = 0

        step = int(frames/image_to_extract)
        for i in range(0, frames, step):
            cv2.imwrite(os.path.join(image_folder_task, f"p{pid}_t{task}_n{video_num}_f{i}.tiff"), buf[i,:,:])
            j = j + 1
            if j == image_to_extract: break
    else:
        messagebox.showerror("Error", "N° of selected frames exeeds the max N° of video frames")


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

label_slice = Label(window,
                    text = "Select n° of frames:",
                    background = "#D1F2EB",
                    fg = "#154360").grid(row = 3)

frame = Entry(window)

button_slice = Button(window,
                     text = "Start Slice",
                     background = "#48C9B0",
                     command = slicing )




label_file_explorer.grid(column = 2, row = 1)

button_explore_dataset.grid(column = 2, row= 2)

button_explore_video.grid(column = 2, row = 3)

frame.grid(column = 2,row = 4)

button_slice.grid(column = 2,row = 5)

window.mainloop()








#parent = 'C:\\Users\matte\Google Drive\Segmentazione PoliMi'
#folder = 'Dataset'
#os.mkdir(os.path.join(parent, folder))
