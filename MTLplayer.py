from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

window = Tk()
window.title("MTLPlayer v. 0.1")
window.iconbitmap('C:/Users/Uzver-PC/PycharmProjects/pythonProject3/MTLPlayer.ico')
window.geometry('520x400')

#mixer init
pygame.mixer.init()

#Song lenght time info
def play_time():
    # Check for double timing
    if stopped:
        return
    #Get elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000
    #slider_label.config(text=f'Slider: {int(slider.get())} and Song Position: {int(current_time)}')
    #Current_time in time format
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))

    #Get currently played song
    #current_song = playlist.curselection()
    song = playlist.get(ACTIVE)
    song = f'{song}.mp3'
    #Load song with mutagen
    muta_song = MP3(song)
    #Get song lenght
    global song_lenght
    song_lenght = muta_song.info.length
    # Converted to time format
    converted_song_lenght = time.strftime('%M:%S', time.gmtime(song_lenght))

    #Increase current time by 1 sec
    current_time += 1

    if int(slider.get()) == int(song_lenght):
        time_bar.config(text=f'Прослушано: {converted_song_lenght} ')

    elif paused:
        pass

    elif int(slider.get()) == int(current_time):
        slider_position = int(song_lenght)
        slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_lenght)
        slider.config(to=slider_position, value=int(slider.get()))

        converted_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        time_bar.config(text=f'Прослушано: {converted_time} из {converted_song_lenght} ')

        # Moving by one sec
        next_time = int(slider.get()) + 1
        slider.config(value=next_time)


    #Output time in statusbar
    #time_bar.config(text=f'Прослушано: {converted_time} из {converted_song_lenght} ')

    #Update slider position to current song position

    #slider.config(to=slider_position, value=int(current_time))

    #Update time info
    time_bar.after(1000, play_time)


#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='C:', title='Выберите трек', filetypes=(('mp3 Files', '*.mp3'), ))

    #song name without  directory path
    song = song.replace("C:/Users/Uzver-PC/PycharmProjects/pythonProject3/audio/", "")
    song = song.replace(".mp3", "")

    #add song to playlist
    playlist.insert(END, song)

# add multiple songs function
def add_multi_songs():
    songs = filedialog.askopenfilenames(initialdir='C:', title='Выберите треки', filetypes=(('mp3 Files', '*.mp3'),))
#directory and file info replace
    for song in songs:
        song = song.replace("C:/Users/Uzver-PC/PycharmProjects/pythonProject3/audio/", "")
        song = song.replace(".mp3", "")
        #insert into playlist
        playlist.insert(END, song)


    #play song

def play():
    # Set stopped variable to false to song play
    global stopped
    stopped = False
    song = playlist.get(ACTIVE)
    song = f'{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Call play_time function to get track lenght

    play_time()

    # Update slider position
    #slider_position = int(song_lenght)
    #slider.config(to=slider_position, value=0)


    # Get current volume
    #current_volume = pygame.mixer.music.get_volume()
    #slider_label.config(text=current_volume * 100)

    # Get current volume
    current_volume = pygame.mixer.music.get_volume()

    # Times by 100 to make it easier to work
    current_volume = current_volume * 100

    # slider_label.config(text=current_volume * 100)

    # Change volume graph image
    if int(current_volume) < 1:
        volume_graph.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_graph.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_graph.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_graph.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_graph.config(image=vol4)

    # Stop playing song
global stopped
stopped = False
def stop():
    # Reset time bar and slider
    time_bar.config(text='')
    slider.config(value=0)
    # Stop playing
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)

    # Clear status bar
    time_bar.config(text='')

    # Set stop variable to TRUE
    global stopped
    stopped = True

    #Next track function

def next_track():
    # Reset time bar and slider
    time_bar.config(text='')
    slider.config(value=0)
    next = playlist.curselection()
    next = next[0]+1
    song = playlist.get(next)
    song = f'{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    playlist.selection_clear(0, END)
    playlist.activate(next)
    playlist.selection_set(next, last=None)

    #Previous track function

def prev_track():
    # Reset time bar and slider
    time_bar.config(text='')
    slider.config(value=0)
    prev = playlist.curselection()
    prev = prev[0] - 1
    song = playlist.get(prev)
    song = f'{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    playlist.selection_clear(0, END)
    playlist.activate(prev)
    playlist.selection_set(prev, last=None)

    #Delete track from playlist

def delete_track():
    stop()
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_many_tracks():
    stop()
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

#Create slider function
def slide(x):
    #slider_label.config(text=f'{int(slider.get())} из {int(song_lenght)}')
    song = playlist.get(ACTIVE)
    song = f'{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))

# Create volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

# Get current volume
    current_volume = pygame.mixer.music.get_volume()

    #Times by 100 to make it easier to work
    current_volume = current_volume * 100

    #slider_label.config(text=current_volume * 100)

    # Change volume graph image
    if int(current_volume) < 1:
        volume_graph.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_graph.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_graph.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_graph.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_graph.config(image=vol4)




# Create master frame
master_frame = Frame(window)
master_frame.pack(pady=20)

# Create playlist box
playlist = Listbox(master_frame, bg="black", fg="orange", width=60, selectbackground='blue')
playlist.grid(row=0, column=0)


# Player buttons images
next_btn_img = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/next.png')
prev_btn_img = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/prev.png')
stop_btn_img = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/stop.png')
pause_btn_img = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/pause.png')
play_btn_img = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/play.png')

# Volume slider level images
global vol0
global vol1
global vol2
global vol3
global vol4
vol0 = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/volume0.png')
vol1 = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/volume1.png')
vol2 = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/volume2.png')
vol3 = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/volume3.png')
vol4 = PhotoImage(file='C:/Users/Uzver-PC/PycharmProjects/pythonProject3/icons/volume4.png')

# Player control frame

control_frame = Frame(master_frame)
control_frame.grid(row=1, column=0, pady=20)

# Create volume level images frame

volume_graph = Label(master_frame, image=vol0)
volume_graph.grid(row=1, column=1, padx=10)

# Player volume frame

volume_frame = LabelFrame(master_frame, text="Громкость")
volume_frame.grid(row=0, column=1, padx=30)

# player buttons control

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

# menu

player_menu = Menu(window)
window.config(menu=player_menu)

# Delete menu
remove_track_menu = Menu(player_menu)
player_menu.add_cascade(label='Удалить из плейлиста', menu=remove_track_menu)
remove_track_menu.add_command(label='Удалить текущий трек из плейлиста', command=delete_track)
remove_track_menu.add_command(label='Удалить все треки из плейлиста', command=delete_many_tracks)


# Add Song menu

add_song_menu = Menu(player_menu)
player_menu.add_cascade(label='Добавить трек(и)', menu=add_song_menu)
add_song_menu.add_command(label='Добавить один трек в плейлист', command=add_song)

# Add Multiple Song menu
add_song_menu.add_command(label='Добавить несколько треков в плейлист', command=add_multi_songs)

# Create Duration bar
time_bar = Label(window, text='', bd=1, relief=GROOVE, anchor=E)
time_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create position slider
slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
slider.grid(row=2, column=0, pady=10)

# Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)



# Create temporary slider label
#slider_label = Label(window, text='0')
#slider_label.pack(pady=17)



window.mainloop()
