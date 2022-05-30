from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import sqlite3


def open_my_shelf(db):
    shelf = Toplevel()
    shelf.title("My shelf")
    shelf.geometry("600x800")
    # Set the resizable property False
    shelf.resizable(False, False)
    # setting background image
    global bg_img
    bg_img = Image.open('images/pexels-emre-can-acer-2079451.jpg')
    [img_width, img_height] = bg_img.size
    bg_img = bg_img.resize((int(img_width * 0.20), int(img_height * 0.20)))
    bg_img = ImageTk.PhotoImage(bg_img)
    canvas = Canvas(shelf)
    canvas.create_image(-50, -200, image=bg_img, anchor=NW)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # frame1 = Frame(shelf, height=1)
    frame2 = Frame(shelf, height=2)
    info_bar = Label(frame2,
                     text=db,
                     bd=1,
                     relief=SUNKEN,
                     anchor=E)
    info_bar.grid(row=2, column=0, columnspan=3, sticky=W + E)
    # Main page buttons
    open_db_btn = Button(shelf, text="Show library", padx=40, pady=30, fg="white", bg="black")
    open_db_btn.pack(pady=(70, 0))
    create_db_btn = Button(shelf, text="Add new item to library", padx=35, pady=30, fg="white", bg="black")
    create_db_btn.pack(pady=(70, 0))
    exit_btn = Button(shelf, text="Back", padx=40, pady=30, command=shelf.destroy, fg="white", bg="black")
    exit_btn.pack(pady=(70, 0))
    frame2.pack(side=BOTTOM, anchor="e", padx=8, pady=8)
