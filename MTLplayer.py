from tkinter import *
import pygame
from tkinter import filedialog

window = Tk()
window.title("MTLPlayer v. 0.1")
window.iconbitmap('C:/Users/Uzver-PC/PycharmProjects/pythonProject3/MTLPlayer.ico')
window.geometry('600x300')

#mixer init
pygame.mixer.init()

#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title='Выберите трек', filetypes=(('mp3 Files', '*.mp3'), ))

    #song name without  directory path
    song = song.replace("C:/Users/Uzver-PC/PycharmProjects/pythonProject3/audio/", "")
    song = song.replace(".mp3", "")

    #add song to playlist
    playlist.insert(END, song)

    #play song

def play():
    song = playlist.get(ACTIVE)
    song = f'C:/Users/Uzver-PC/PycharmProjects/pythonProject3/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Stop playing song

def stop():
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)

    #Global pause variable

    global paused


    # Pause\unpause current song

def pause():
    #pause
    pygame.mixer.music.pause()
    playlist.selection_clear(ACTIVE)

    #unpause
    pygame.mixer.music.unpause()
    playlist.selection_clear(ACTIVE)


#playlist
playlist = Listbox(window, bg="white", fg="black", width=60, selectbackground='gray')
playlist.pack(pady=20)


#player buttons images
next_btn_img = PhotoImage(file='icons/next.png')
prev_btn_img = PhotoImage(file='icons/prev.png')
stop_btn_img = PhotoImage(file='icons/stop.png')
pause_btn_img = PhotoImage(file='icons/pause.png')
play_btn_img = PhotoImage(file='icons/play.png')

#player control frame

control_frame = Frame(window)
control_frame.pack()

#player buttons control

next_btn = Button(control_frame, image=next_btn_img, borderwidth=0)
prev_btn = Button(control_frame, image=prev_btn_img, borderwidth=0)
stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause)
play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)

next_btn.grid(row=0, column=4, padx=5)
prev_btn.grid(row=0, column=0, padx=5)
stop_btn.grid(row=0, column=1, padx=5)
pause_btn.grid(row=0, column=3, padx=5)
play_btn.grid(row=0, column=2, padx=5)

#menu

player_menu = Menu(window)
window.config(menu=player_menu)

#Add Song menu

add_song_menu = Menu(player_menu)
player_menu.add_cascade(label='Добавить треки', menu=add_song_menu)
add_song_menu.add_command(label='Добавить один трек в плейлист', command=add_song)













window.mainloop()
