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

# add multiple songs function
def add_multi_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title='Выберите треки', filetypes=(('mp3 Files', '*.mp3'),))
#directory and file info replace
    for song in songs:
        song = song.replace("C:/Users/Uzver-PC/PycharmProjects/pythonProject3/audio/", "")
        song = song.replace(".mp3", "")
        #insert into playlist
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

    #Next track function

def next_track():
    next = playlist.curselection()
    next = next[0]+1
    song = playlist.get(next)
    song = f'C:/Users/Uzver-PC/PycharmProjects/pythonProject3/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    playlist.selection_clear(0, END)
    playlist.activate(next)
    playlist.selection_set(next, last=None)

    #Previous track function

def prev_track():
    prev = playlist.curselection()
    prev = prev[0] - 1
    song = playlist.get(prev)
    song = f'C:/Users/Uzver-PC/PycharmProjects/pythonProject3/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    playlist.selection_clear(0, END)
    playlist.activate(prev)
    playlist.selection_set(prev, last=None)

    #Delete track from playlist

def delete_track():
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_many_tracks():
    playlist.delete(0,END)
    pygame.mixer.music.stop()



#Global pause variable

global paused
paused = False


    # Pause\unpause current song

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
       #pause
        pygame.mixer.music.pause()
        paused = True



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

next_btn = Button(control_frame, image=next_btn_img, borderwidth=0, command=next_track)
prev_btn = Button(control_frame, image=prev_btn_img, borderwidth=0, command=prev_track)
stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)

next_btn.grid(row=0, column=4, padx=5)
prev_btn.grid(row=0, column=0, padx=5)
stop_btn.grid(row=0, column=1, padx=5)
pause_btn.grid(row=0, column=3, padx=5)
play_btn.grid(row=0, column=2, padx=5)

#menu

player_menu = Menu(window)
window.config(menu=player_menu)

#Delete menu
remove_track_menu = Menu(player_menu)
player_menu.add_cascade(label='Удалить из плейлиста', menu=remove_track_menu)
remove_track_menu.add_command(label='Удалить один трек из плейлиста', command=delete_track)
remove_track_menu.add_command(label='Удалить все треки из плейлиста', command=delete_many_tracks)


#Add Song menu

add_song_menu = Menu(player_menu)
player_menu.add_cascade(label='Добавить трек(и)', menu=add_song_menu)
add_song_menu.add_command(label='Добавить один трек в плейлист', command=add_song)

#Add Multiple Song menu
add_song_menu.add_command(label='Добавить несколько треков в плейлист', command=add_multi_songs)














window.mainloop()
