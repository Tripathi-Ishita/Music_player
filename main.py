import os
import threading
import time
import tkinter
from tkinter import filedialog
from tkinter.ttk import Progressbar

import pygame
from mutagen.mp3 import MP3

pygame.mixer.init()
current_position = 0
paused = False
selected_Folder_path = ""


def select_music_folder():
    global selected_Folder_path
    selected_Folder_path = filedialog.askdirectory()
    if selected_Folder_path:
        lbox.delete(0, tkinter.END)
        for filename in os.listdir(selected_Folder_path):
            if filename.endswith(".mp3"):
                lbox.insert(tkinter.END, filename)


def update_progress():
    global current_position
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current_position = pygame.mixer.music.get_pos() / 1000
            pbar["value"] = current_position
            window.update_idletasks()  # Update the progress bar
            if current_position >= pbar["maximum"]:
                stop_music()
                pbar["value"] = 0
        time.sleep(0.1)


pt = threading.Thread(target=update_progress)
pt.daemon = True
pt.start()


def stop_music():
    global paused
    pygame.mixer.music.stop()
    paused = False


def previous_song():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index > 0:
            lbox.selection_clear(0, tkinter.END)
            lbox.selection_set(current_index - 1)
            play_selected_song()


def play_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        play_selected_song()


def play_selected_song():
    global current_position, paused
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        selected_song = lbox.get(current_index)
        full_path = os.path.join(selected_Folder_path, selected_song)
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(start=current_position)
        paused = False
        audio = MP3(full_path)
        song_duration = audio.info.length
        pbar["maximum"] = song_duration


def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True


def next_song():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index < lbox.size() - 1:
            lbox.selection_clear(0, tkinter.END)
            lbox.selection_set(current_index + 1)
            play_selected_song()


window = tkinter.Tk()
window.title("Music Player App")
window.geometry("700x700")
window["bg"] = "pink"

heart_icon = tkinter.PhotoImage(file="image/mu.png")
heart_icon = heart_icon.subsample(3)
image_label = tkinter.Label(window, image=heart_icon)
image_label.place(relx=0.05, rely=0.02)
l_music_player = tkinter.Label(window, text="Music Player",font=("Comic Sans MS", 30, "bold"))
l_music_player.pack(pady=10)
btn_select_folder = tkinter.Button(window, text="Select Music Folder",
                                   command=select_music_folder,
                                   font=("Comic Sans MS", 18))
btn_select_folder.pack(pady=20)
lbox = tkinter.Listbox(window, width=50, font=("Comic Sans MS", 16))
lbox.pack(pady=10)
btn_frame = tkinter.Frame(window)
btn_frame.pack(pady=20)
btn_previous = tkinter.Button(btn_frame, text="<", command=previous_song,
                              width=10, font=("Comic Sans MS", 18))
btn_previous.pack(side=tkinter.LEFT, padx=5)
btn_play = tkinter.Button(btn_frame, text="Play", command=play_music,
                          width=10, font=("Comic Sans MS", 18))
btn_play.pack(side=tkinter.LEFT, padx=5)
btn_pause = tkinter.Button(btn_frame, text="Pause", command=pause_music,
                           width=10, font=("Comic Sans MS", 18))
btn_pause.pack(side=tkinter.LEFT, padx=5)
btn_next = tkinter.Button(btn_frame, text=">", command=next_song,
                          width=10, font=("Comic Sans MS", 18))
btn_next.pack(side=tkinter.LEFT, padx=2)
pbar = Progressbar(window, length=300, mode="determinate")
pbar.pack()
window.mainloop()
