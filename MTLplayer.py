from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

window = Tk()
window.title("MTLPlayer v. 0.1")
window.iconbitmap('C:/Users/Uzver-PC/PycharmProjects/pythonProject3/MTLPlayer.ico')
window.geometry('600x450')

#mixer init
pygame.mixer.init()

#Song lenght time info
def play_time():
    #Get elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000
    #Current_time in time format
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))

    #Get currently played song
    #current_song = playlist.curselection()
    song = playlist.get(ACTIVE)
    song = f'C:/Users/Uzver-PC/PycharmProjects/pythonProject3/audio/{song}.mp3'
    #Load song with mutagen
    muta_song = MP3(song)
    #Get song lenght
    global song_lenght
    song_lenght = muta_song.info.length
    # Converted to time format
    converted_song_lenght = time.strftime('%M:%S', time.gmtime(song_lenght))

    #Output time in statusbar
    time_bar.config(text=f'Прослушано: {converted_time} из {converted_song_lenght} ')
    # Update slider position to current song position
    slider.config(value=int(current_time))

    #Update time info
    time_bar.after(1000, play_time)


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

    # Call play_time function to get track lenght

    play_time()

    # Update slider position
    slider_position = int(song_lenght)
    slider.config(to=slider_position, value=0)



    # Stop playing song

def stop():
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)

    #Clear status bar
    time_bar.config(text='')

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

#Creat slider function
def slide(x):
    slider_label.config(text=f'{int(slider.get())} из {int(song_lenght)}')

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
remove_track_menu.add_command(label='Удалить текущий трек из плейлиста', command=delete_track)
remove_track_menu.add_command(label='Удалить все треки из плейлиста', command=delete_many_tracks)


#Add Song menu

add_song_menu = Menu(player_menu)
player_menu.add_cascade(label='Добавить трек(и)', menu=add_song_menu)
add_song_menu.add_command(label='Добавить один трек в плейлист', command=add_song)

#Add Multiple Song menu
add_song_menu.add_command(label='Добавить несколько треков в плейлист', command=add_multi_songs)

#Create Duration bar
time_bar = Label(window, text='', bd=1, relief=GROOVE, anchor=E)
time_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Create position slider
slider = ttk.Scale(window, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
slider.pack(pady=15)

#Create temporary slider label
slider_label=Label(window, text='0')
slider_label.pack(pady=17)











window.mainloop()
