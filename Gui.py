from tkinter import *
from tkinter.filedialog import askopenfilename
import pygame
from mutagen.mp3 import MP3
import time


class GUI:
    def __init__(self, master):
        self.master = master
        global audio_file_list, paused
        paused = False
        audio_file_list = []

#-------PyGame----------------
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.mixer.music.set_volume(.3)


#-------GUI-LAYOUT------------
        master.title("MP3 Player")
        master.geometry('400x300')

#-------LABELS----------------
        self.start = Label(master, text="0:00", width=3, height=1, justify=CENTER)
        self.start.grid(row=0, column=0, sticky=W, columnspan=2)
        self.end = Label(master, textvariable=length, width=3, height=1, justify=CENTER)
        self.end.grid(row=0, column=19, sticky=W, columnspan=2)

#-------Buttons---------------
        self.play_image = PhotoImage(file='Images/Play.png')
        self.play_button = Button(master, image=self.play_image, width=20, height=20, anchor="w", command=self.playAudio)
        self.play_button.grid(row=1, column=0, columnspan=2,  sticky=N)

        self.pause_image = PhotoImage(file='Images/Pause.png')
        self.pause_button = Button(master, image=self.pause_image, width=20, height=20, anchor="w", command=self.pauseAudio)
        self.pause_button.grid(row=1, column=2, columnspan=2, sticky=N)

        self.stop_image = PhotoImage(file='Images/Stop.png')
        self.stop_button = Button(master, image=self.stop_image, width=20, height=20, anchor="w", command=self.stopAudio)
        self.stop_button.grid(row=1, column=4, columnspan=2, sticky=N)

        self.back_image = PhotoImage(file='Images/Back.png')
        self.back_button = Button(master, image=self.back_image, width=30, height=20, command=self.backwardAudio)
        self.back_button.grid(row=1, column=6, columnspan=3, sticky=W)

        self.forward_image = PhotoImage(file='Images/Forward.png')
        self.forward_button = Button(master, image=self.forward_image, width=30, height=20, command=self.forwardAudio)
        self.forward_button.grid(row=1, column=8, columnspan=3, sticky=E)

        self.add_button = Button(text="Add", width=10, height=1, command=self.addAudioFile)
        self.add_button.grid(row=4, column=0, columnspan=10, sticky=W)

        self.remove_button = Button(master, text="Remove", width=10, height=1, command=self.removeAudio)
        self.remove_button.grid(row=4, column=10, columnspan=10, sticky=W)
#-------Scales----------------
        self.volume_scale = Scale(master, from_=0, to=100, length=130, orient=HORIZONTAL, showvalue=0, command=self.setVolume)
        self.volume_scale.grid(row=1, column=11, sticky=W, columnspan=10)

#-------Lists-----------------
        self.music_list = Listbox(master, width=48, borderwidth=3)
        self.music_list.grid(row=3, column=0, columnspan=20, sticky=W)

#-------FUNCTIONS-------------
    def addAudioFile(self):
        audio_file = askopenfilename()
        audio_name = audio_file.split('/')
        audio_name = audio_name[len(audio_name)-1]
        self.music_list.insert(END, audio_name)
        audio_file_list.append(audio_file)

    def updateTimeScale(self):
        temp = MP3(audio_file_list[self.music_list.index(ACTIVE)])
        temp = int(temp.info.length)
        self.time_scale.config(to=temp)

    def updateEnd(self):
        temp = MP3(audio_file_list[self.music_list.index(ACTIVE)])
        temp = int(temp.info.length)
        length.set(time.strftime('%M:%S', time.gmtime(temp)))

    def playAudio(self):
        global paused
        if paused:
            pygame.mixer.music.unpause()
            paused = False
        elif len(audio_file_list) != 0:
            pygame.mixer.music.load(audio_file_list[self.music_list.index(ACTIVE)])
            pygame.mixer.music.play()
        else:
            print('No Audio Loaded')
        self.updateEnd()

    def removeAudio(self):
        if len(audio_file_list) != 0:
            print(self.music_list.index(ACTIVE))
            audio_file_list.remove(audio_file_list[self.music_list.index(ACTIVE)])
            self.music_list.delete(ACTIVE)
        else:
            print('Nothing to remove')

    def setVolume(self, vol):
        volume = int(vol) / 100
        pygame.mixer.music.set_volume(volume)

    def pauseAudio(self):
        global paused
        paused = True
        pygame.mixer.music.pause()

    def stopAudio(self):
        pygame.mixer.music.stop()

    def forwardAudio(self):
        if len(audio_file_list) == 0:
            print('No Audio Loaded')
        elif self.music_list.index(ACTIVE)+1 < len(self.music_list.get(0, END)):
            self.music_list.activate(self.music_list.index(ACTIVE)+1)
            pygame.mixer.music.load(audio_file_list[self.music_list.index(ACTIVE)])
            pygame.mixer.music.play()
        else:
            self.music_list.activate(0)
            pygame.mixer.music.load(audio_file_list[0])
            pygame.mixer.music.play()
        self.updateEnd()

    def backwardAudio(self):
        if len(audio_file_list) == 0:
            print('No Audio Loaded')
        elif self.music_list.index(ACTIVE)-1 > 0:
            self.music_list.activate(self.music_list.index(ACTIVE)-1)
            pygame.mixer.music.load(audio_file_list[self.music_list.index(ACTIVE)])
            pygame.mixer.music.play()
        else:
            self.music_list.activate(0)
            pygame.mixer.music.load(audio_file_list[0])
            pygame.mixer.music.play()
        self.updateEnd()


root = Tk()
length = StringVar()
my_gui = GUI(root)
root.mainloop()
