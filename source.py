from tkinter import *
import time
import sys
from tkinter import filedialog
from pygame import mixer
import datetime


#Global var
cur_music = ""
is_play = False
cur_vol = 1
is_loop = 0

mixer.init()


def open_song():
    global is_play
    global cur_vol
    global is_loop
    global cur_music
    cur_music = filedialog.askopenfilename(initialdir = "C:\\Users\\nguye\\Music", title = "Open The Song")
    temp_arr = cur_music.split("/")
    name_music = temp_arr[len(temp_arr) - 1]
    print(name_music)
    try:
        mixer.music.load(cur_music)
        is_play = True
        mixer.music.play(loops=is_loop)
        mixer.music.set_volume(cur_vol)
        music_list.insert(1, name_music)
    except:
        pass

def pause_play():
    global is_play
    if is_play == False:
        is_play = True
        mixer.music.unpause()
    else:
        is_play = False
        mixer.music.pause()

def reduce_vol():
    global cur_vol
    if cur_vol == 0:
        return
    else:
        cur_vol -= 0.1
        volume_label.config(text = f"Volume: {int(cur_vol * 100)}%")
        mixer.music.set_volume(cur_vol)

def increase_vol():
    global cur_vol
    if cur_vol == 1:
        return
    else:
        cur_vol += 0.1
        volume_label.config(text = f"Volume: {int(cur_vol * 100)}%")
        mixer.music.set_volume(cur_vol)

def startLoop():
    global is_loop
    if is_loop == 0:
        is_loop = -1
    else:
        is_loop = 0

def fast_forward():
    mixer.music.play()
    mixer.music.pause()
    cur_time = mixer.music.get_pos() / 1000
    print(cur_time)
    mixer.music.set_pos(cur_time + 10)
    mixer.music.unpause()


class Object():
    def __init__(self,canvas, x, y, xVeclocity, yVeclocity, photo, canPass):
        self.canvas = canvas
        self.image = canvas.create_image(x, y, image = photo, anchor = NW)
        self.canPass = canPass
        self.xVeclocity = xVeclocity
        self.yVeclocity = yVeclocity
        self.photo = photo
        self.x = x
        self.y = y
    def move(self):
        coordinates = self.canvas.coords(self.image)
        if (self.canPass == True):
            if (coordinates[1] < -300):
                self.canvas.delete(self.image)
                self.image = canvas.create_image(self.x, self.y, image=self.photo, anchor=NW)
        pause_but.update()
        self.canvas.update()
        if (self.canPass == False):
            if coordinates[0] >= self.canvas.winfo_width() - self.photo.width() or coordinates[0] < 0:
                self.xVeclocity = -self.xVeclocity
            if coordinates[1] >= self.canvas.winfo_height() - self.photo.height() or coordinates[1] < 0:
                self.yVeclocity = -self.yVeclocity
        self.canvas.move(self.image, self.xVeclocity, self.yVeclocity)
        window.update()
        time.sleep(0.01)

if __name__ == "__main__":

    #Init window
    window = Tk()
    window.config(bg = "white")
    window.title("Music Player")
    window.geometry("1000x800")
    window.resizable(False, False)

    canvas = Canvas(window, width = 1000, height = 800)
    background = PhotoImage(file = "img//background.png")
    canvas.create_image(0, 0, image = background, anchor = NW)

    label = Label(window,
                text = "MUSIC PLAYER",
                font = ("Ink Free", 50, "bold", "italic"),
                bg = "white",
                fg = "#ff0066")
    label.pack()
    canvas.pack()

    photo1 = PhotoImage(file = "img//em1.png").subsample(2, 2)
    photo2 = PhotoImage(file = "img//em2.png").subsample(5, 5)
    photo3 = PhotoImage(file = "img//em3.png").subsample(5, 5)

    object1 = Object(canvas, 150, 600, 0, -3, photo1, True)
    object2 = Object(canvas, 450, 600, 0, -6, photo1, True)
    object3 = Object(canvas, 750, 600, 0, -4, photo1, True)
    object4 = Object(canvas, 0, 0, 6, 8,photo2, False)
    object5 = Object(canvas, 0, 0, 8, 6, photo3, False)

    menuBar = Menu(window)
    window.config(menu = menuBar)

    fileMenu = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label="File", menu = fileMenu)
    fileMenu.add_command(label = "Open The Song", command = open_song)


    pause_img = PhotoImage(file = "img//pause.png").subsample(10, 10)
    pause_but = Button(canvas, image = pause_img, command = pause_play)
    canvas.update()
    pause_but.place(x = int(canvas.winfo_width()/2 - 100 / 2), y = int(canvas.winfo_height()/2 - 100 / 2))

    volume_label = Label(canvas, text = f"Volume: {cur_vol * 100}%", font = ("Ink Free", 40))
    volume_label.place(x = 350, y = 600)

    reduce_vol_but = Button(canvas, text = "-", font = ("Ink Free", 40), width = 3, height = 1, command = reduce_vol)
    increase_vol_but = Button(canvas, text = "+", font = ("Ink Free", 40), width = 3, height = 1, command = increase_vol)
    volume_label.update()
    reduce_vol_but.place(x = int(volume_label.winfo_x() - 100) - 120, y = 600)
    increase_vol_but.place(x = int(volume_label.winfo_x() + volume_label.winfo_width() + 100), y = 600)

    loop_img = PhotoImage(file = "img//loops.png").subsample(4, 4)
    loop_but = Button(canvas, image = loop_img, command = startLoop)
    loop_but.place(x = canvas.winfo_width() - loop_img.width(), y = int(canvas.winfo_height()/2 - 100 / 2))

    ahead_but = Button(canvas, text = "Tua nhanh", command = fast_forward)
    ahead_but.place(x = int(canvas.winfo_width()/2 - 100 / 2) + 200, y = int(canvas.winfo_height()/2 - 100 / 2))

    music_list = Listbox(canvas)
    music_list.place(x = 0, y = 0)

    while True:
        object1.move()
        object2.move()
        object3.move()
        object4.move()
        object5.move()

    window.mainloop()