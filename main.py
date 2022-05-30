from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import os
import sqlite3
import myshelf_main


root = Tk()
root.title("My library manager")
root.geometry("600x800")
# Set the resizable property False
root.resizable(False, False)
# setting background image
global bg_img
bg_img = Image.open('images/pexels-emre-can-acer-2079451.jpg')
[img_width, img_height] = bg_img.size
bg_img = bg_img.resize((int(img_width * 0.20), int(img_height * 0.20)))
bg_img = ImageTk.PhotoImage(bg_img)
canvas = Canvas(root)
canvas.create_image(-50, -200, image=bg_img, anchor=NW)
canvas.place(x=0, y=0, relwidth=1, relheight=1)


# open existing database
def open_db():
    root.filename = filedialog.askopenfilename(
                                    initialdir="db/",
                                    title="Select a file:",
                                    filetypes=(("database files", "*.db"),)
                                    )

    myshelf_main.open_my_shelf(root.filename)


# create new database
def create_db():
    # create database with defined name
    def create_db_ok(event=None):
        # check if default folder with db files does exist else it will be created
        db_path = "db/"
        dir_status = os.path.exists(db_path)
        if dir_status is False:
            os.makedirs(db_path)

        # check if new database name already exists before creating it
        new_db = f'db/{create_db_entry.get()}.db'
        if not os.path.exists(new_db):
            # checking if the new database is created and opens properly
            try:
                # Create a database
                conn = sqlite3.connect(f'db/{create_db_entry.get()}.db')
            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Error while creating database, please avoid special characters")
            else:
                # Create cursor
                c = conn.cursor()

                # Create table album
                c.execute("""
                            CREATE TABLE "album" (
                            "title"	TEXT NOT NULL,
                            "artist_name"	TEXT NOT NULL,
                            "year"	INTEGER,
                            "genre"	TEXT,
                            "format"    TEXT,
                            "cover"	BLOB)
                            """)

                # Create table books
                c.execute("""
                            CREATE TABLE "books" (
                            "title"	TEXT NOT NULL,
                            "author"	TEXT,
                            "year"	INTEGER,
                            "publisher"	TEXT)
                            """)

                # Create table films
                c.execute("""
                            CREATE TABLE "films" (
                            "title"	TEXT NOT NULL,
                            "year"	INTEGER,
                            "film_info"	TEXT,
                            "cover"	BLOB)
                            """)

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                messagebox.showinfo("Info", f"Your database {create_db_entry.get()}.db has been created successfully!")

                create_db_win.destroy()

                myshelf_main.open_my_shelf(new_db)
        else:
            messagebox.showwarning("Warning", "This database name already exists!")

    # Create new windows to set new database name
    create_db_win = Toplevel(root)
    create_db_win.geometry("250x120")
    create_db_win.title("Create new database")

    # Binding confirm_create_db_btn with Enter key
    create_db_win.bind('<Return>', create_db_ok)

    # DB creation page buttons
    create_db_label = Label(create_db_win, text="Set a name for your new database:")
    create_db_label.grid(row=0, columnspan=2, padx=5, pady=5)
    create_db_entry = Entry(create_db_win)
    create_db_entry.grid(row=1, columnspan=2, padx=5, pady=5)
    create_db_entry.focus_set()
    confirm_create_db_btn = Button(create_db_win, text="Create database", command=create_db_ok)
    confirm_create_db_btn.grid(row=2, column=0, padx=5, pady=5)
    create_db_exit = Button(create_db_win, text="Back", command=create_db_win.destroy)
    create_db_exit.grid(row=2, column=1, padx=5, pady=5)


# Main page buttons
open_db_btn = Button(root, text="Open database", padx=40, pady=30, command=open_db, fg="white", bg="black")
open_db_btn.pack(pady=(70, 0))
create_db_btn = Button(root, text="Create database", padx=35, pady=30, command=create_db, fg="white", bg="black")
create_db_btn.pack(pady=(70, 0))
exit_btn = Button(root, text="Exit", padx=40, pady=30, command=root.quit, fg="white", bg="black")
exit_btn.pack(pady=(70, 0))


root.mainloop()
