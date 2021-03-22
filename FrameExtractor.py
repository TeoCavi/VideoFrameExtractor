from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
import os
import shutil
import numpy as np

BACKGROUND = "#6495ED"


def BrowseDataset(): #Funzione invocata alla pressione del pulsante "Browse Dataset"
    global dataset_dir
    dataset_dir = filedialog.askdirectory() #salva in dataset_dir la directory del dataset


def DirectoryCreation(): #Funzione invocata alla pressione del pulsante "Browse Video"
    global cap, frameCount
    global image_folder_task
    global pid, task, video_num

    filetype = (("avi files", "*.avi"), ("all files", "*.*"))
    filename = filedialog.askopenfilename(initialdir = "/",     #salva in filename il nome del video con la sua collocazione
                                          title = "Select Video",
                                          filetypes = filetype )

    full_name = os.path.basename(filename) #salva in full_name solo il nome del video
    name = os.path.splitext(full_name)[0] #salva in name solo il nome del video (senza l'estensione .avi)
    fname = name.split("_") #fname è una lista i cui elementi sono le parti del nome del video (ID paziente, task, numero del video)

    pid = str(fname[0]) #salva in pid solo l'ID del paziente (castato a stringa)
    task = fname[1] #salva in task solo il nome della task
    video_num = str(fname[2]) #salva in video_num solo il numero del video (castato a stringa)

    patients = next(os.walk(dataset_dir))[1] #salva in patients i nomi delle cartelle contenute in Dataset

    patient_dir = os.path.join(dataset_dir, f"Patient_{pid}") #cartella Patient_ID
    first_level_dir = ["Video","Images","Segmentations"] #Cartelle contenute nella cartella Patient_ID
    video_folder = os.path.join(patient_dir, first_level_dir[0]) #cartella Video
    image_folder = os.path.join(patient_dir, first_level_dir[1]) #cartella Images
    segmentation_folder = os.path.join(patient_dir, first_level_dir[2]) #cartella Segmentations
    video_folder_task = os.path.join(video_folder, task) #cartella task nella cartella Video
    image_folder_task = os.path.join(image_folder, task) #cartella task nella cartella Images
    segmentation_folder_task = os.path.join(segmentation_folder, task) #cartella task nella cartella Segmentations

    new_patient = 1
    for patient in patients:
        if (patient == f"Patient_{pid}"): #se il nuovo video riguarda un paziente già presente nel Dataset
            new_patient = 0

    if new_patient == 1: #nuovo paziente nel database
        case = "NewPatient"
        os.mkdir(patient_dir) #crea la cartella Patient_ID
        os.mkdir(video_folder) #crea la cartella Video
        os.mkdir(image_folder) #crea la cartella Images
        os.mkdir(segmentation_folder) #crea la cartella Segmentations
        os.mkdir(video_folder_task) #crea la cartella task nella cartella Video
        os.mkdir(image_folder_task) #crea la cartella task nella cartella Images
        os.mkdir(segmentation_folder_task) #crea la cartella task nella cartella Segmentations
        shutil.copy(filename, video_folder_task) #copia il video nnella cartella task della cartella Video

    if new_patient == 0: #paziente già inserito
        tasks = next(os.walk(video_folder))[1] #salva in tasks i nomi delle cartelle contenute in Video

        case = "NewVideoDiffTask"
        for t in tasks:
            if t == task: #se la task è già presente
                videos = next(os.walk(video_folder_task))[2] #salva in videos i nomi delle cartelle contenute nella cartella task in Video
                case = "NewVideoSameTask"
                for v in videos:
                    if v == full_name: #se il video è già presente
                        case = "ChangeNumFrame"

                if(case == "NewVideoSameTask"): #se si tratta di un altro video della stessa task
                    shutil.copy(filename, video_folder_task) #copia il video nella cartella task della cartella Video

        if (case == "NewVideoDiffTask"): #se si tratta di una task diversa
            os.mkdir(video_folder_task) #crea la cartella task nella cartella Video
            os.mkdir(image_folder_task) #crea la cartella task nella cartella Images
            os.mkdir(segmentation_folder_task) #crea la cartella task nella cartella Segmentations
            shutil.copy(filename, video_folder_task) #copia il video nella cartella task della cartella Video

    cap = cv2.VideoCapture(os.path.join(video_folder_task,full_name)) # video salvato in cap
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #numero totale di frame salvato in frameCount

    label_file_explorer.configure(text=f"Patient n°: {pid}\n N° of frames: {frameCount}\n Case: {case}  ",
                                  width = 100, height = 6)



def slicing(): #Funzione invocata alla pressione del pulsante "Start Slice"

    if(int(frame.get())>1 and int(frame.get())<frameCount):

        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #larghezza immagine in pixel
        frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #altezza immagine in pixel

        buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8')) #buffer buf
        fc = 0
        ret = True

        while (fc < frameCount  and ret):
            ret, buf[fc] = cap.read() #frames salvate nel buffer buf
            fc += 1

        cap.release()

        frames = buf.shape[0] #numero di frame salvato in  frames
        image_to_extract = int(frame.get()) #numero di frame inserite dall'utente salvate in image_to_extract

        fc = 0
        ret = True
        j = 0

        step = int(frames/image_to_extract)
        for i in range(0, frames, step):
            cv2.imwrite(os.path.join(image_folder_task, f"p{pid}_t{task}_n{video_num}_f{i}.tiff"), buf[i,:,:]) #salva le immagini nella cartella task nella cartella Images
            j = j + 1
            if j == image_to_extract: break
    else:
        messagebox.showerror("Error", "N° of selected frames exeeds the max N° of video frames")

# GRAFICA

window = Tk()
window.title('Video Slicer')
window.config(background = BACKGROUND)
#window.geometry("500x500")
window.grid_columnconfigure(10, minsize=100)
window.grid_rowconfigure(10, minsize=100)

#LABELS

label_file_explorer = Label(window,
                            text = "Video Slicer",
                            width = 100, height = 4,
                            background = BACKGROUND,
                            fg = "#154360")

label_slice = Label(window,
                    text = "Select n° of frames:",
                    background = "#D1F2EB",
                    fg = "#154360")

#BUTTONS

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
                    background = BACKGROUND,
                    fg = "#154360").grid(row = 3)

frame = Entry(window)

button_slice = Button(window,
                     text = "Start Slice",
                     background = "#48C9B0",
                     command = slicing )

frame = Entry(window)


label_file_explorer.grid(column = 2, row = 1)

label_slice.grid(column = 1, row = 4)

button_explore_dataset.grid(column = 2, row= 2)

button_explore_video.grid(column = 2, row = 3)

button_slice.grid(column = 2,row = 5)

frame.grid(column = 2,row = 4)

window.mainloop()








#parent = 'C:\\Users\matte\Google Drive\Segmentazione PoliMi'
#folder = 'Dataset'
#os.mkdir(os.path.join(parent, folder))
