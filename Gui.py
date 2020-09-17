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

        # -------PyGame----------------
        # initialize mixer module
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        # initialize pygame module
        pygame.init()
        pygame.mixer.music.set_volume(.3)

        # -------GUI-LAYOUT------------
        master.title("MP3 Player")
        master.geometry('400x300')

        # -------LABELS----------------
        self.start = Label(master, text="0:00", width=3,
                           height=1, justify=CENTER)
        self.start.grid(row=0, column=0, sticky=W, columnspan=2)
        self.end = Label(master, textvariable=length,
                         width=3, height=1, justify=CENTER)
        self.end.grid(row=0, column=19, sticky=W, columnspan=2)

        # -------Buttons---------------
        self.play_image = PhotoImage(file='Images/Play.png')
        self.play_button = Button(master, image=self.play_image,
                                  width=20, height=20, anchor="w", command=self.playAudio)
        self.play_button.grid(row=1, column=0, columnspan=2, sticky=N)

        self.pause_image = PhotoImage(file='Images/Pause.png')
        self.pause_button = Button(master, image=self.pause_image,
                                   width=20, height=20, anchor="w", command=self.pauseAudio)
        self.pause_button.grid(row=1, column=2, columnspan=2, sticky=N)

        self.stop_image = PhotoImage(file='Images/Stop.png')
        self.stop_button = Button(master, image=self.stop_image,
                                  width=20, height=20, anchor="w", command=self.stopAudio)
        self.stop_button.grid(row=1, column=4, columnspan=2, sticky=N)

        self.back_image = PhotoImage(file='Images/Back.png')
        self.back_button = Button(
            master, image=self.back_image, width=30, height=20, command=self.backwardAudio)
        self.back_button.grid(row=1, column=6, columnspan=3, sticky=W)

        self.forward_image = PhotoImage(file='Images/Forward.png')
        self.forward_button = Button(
            master, image=self.forward_image, width=30, height=20, command=self.forwardAudio)
        self.forward_button.grid(row=1, column=8, columnspan=3, sticky=E)

        self.add_button = Button(text="Add", width=10,
                                 height=1, command=self.addAudioFile)
        self.add_button.grid(row=4, column=0, columnspan=10, sticky=W)

        self.remove_button = Button(
            master, text="Remove", width=10, height=1, command=self.removeAudio)
        self.remove_button.grid(row=4, column=10, columnspan=10, sticky=W)
        # -------Scales----------------
        self.volume_scale = Scale(master, from_=0, to=100, length=130,
                                  orient=HORIZONTAL, showvalue=0, command=self.setVolume)
        self.volume_scale.grid(row=1, column=11, sticky=W, columnspan=10)

        # -------Lists-----------------
        self.music_list = Listbox(master, width=48, borderwidth=3)
        self.music_list.grid(row=3, column=0, columnspan=20, sticky=W)

    # -------FUNCTIONS-------------
    def addAudioFile(self):
        audio_file = askopenfilename()
        audio_name = audio_file.split('/')  # split file path
        audio_name = audio_name[len(audio_name) - 1]  # get last item
        self.music_list.insert(END, audio_name)  # insert music name into listbox
        audio_file_list.append(audio_file)  # insert audio file name into array

    def updateEnd(self):
        temp = MP3(audio_file_list[self.music_list.index(ACTIVE)])  # get active file
        temp = int(temp.info.length)  # get length
        length.set(time.strftime('%M:%S', time.gmtime(temp)))  # set label to length

    def playAudio(self):
        global paused
        if paused:  # if paused then unpause
            pygame.mixer.music.unpause()
            paused = False
        elif len(audio_file_list) != 0:  # else load active file
            pygame.mixer.music.load(
                audio_file_list[self.music_list.index(ACTIVE)])
            pygame.mixer.music.play()  # play if exists
        else:
            print('No Audio Loaded')
        self.updateEnd()

    def removeAudio(self):
        if len(audio_file_list) != 0:  # if array not empty remove active item, else nothing to remove
            print(self.music_list.index(ACTIVE))
            audio_file_list.remove(
                audio_file_list[self.music_list.index(ACTIVE)])
            self.music_list.delete(ACTIVE)
            self.stopAudio()
        else:
            print('Nothing to remove')

    def setVolume(self, vol):  # convert volume to a scale of 100 then set to scrollbar value
        volume = int(vol) / 100
        pygame.mixer.music.set_volume(volume)

    @staticmethod
    def pauseAudio():  # set global paused to True and pause audio
        global paused
        paused = True
        pygame.mixer.music.pause()

    @staticmethod  # Stop mixer
    def stopAudio():
        pygame.mixer.music.stop()

    def forwardAudio(self):
        if len(audio_file_list) == 0:  # if file array not empty
            print('No Audio Loaded')
        elif self.music_list.index(ACTIVE) + 1 < len(self.music_list.get(0, END)):  # check if next file exists in array
            self.music_list.activate(self.music_list.index(ACTIVE) + 1)  # if so then load next file and play
            pygame.mixer.music.load(
                audio_file_list[self.music_list.index(ACTIVE)])
            pygame.mixer.music.play()
        else:  # else set active to 1st item and load and play
            self.music_list.activate(0)
            pygame.mixer.music.load(audio_file_list[0])
            pygame.mixer.music.play()
        self.updateEnd()  # set label time for next audio file

    def backwardAudio(self):
        if len(audio_file_list) == 0:  # if file array not empty
            print('No Audio Loaded')
        elif self.music_list.index(ACTIVE) - 1 > 0:  # check if previous file exists in array
            self.music_list.activate(self.music_list.index(ACTIVE) - 1)  # if so then load previous file and play
            pygame.mixer.music.load(
                audio_file_list[self.music_list.index(ACTIVE)])
            pygame.mixer.music.play()
        else:  # else set active to 1st item and load and play
            self.music_list.activate(0)
            pygame.mixer.music.load(audio_file_list[0])
            pygame.mixer.music.play()
        self.updateEnd()  # set label time for next audio file


root = Tk()
length = StringVar()
my_gui = GUI(root)
root.mainloop()

