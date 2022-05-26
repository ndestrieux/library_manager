from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import sqlite3


root = Tk()
root.title("My library manager")
# icon = PhotoImage(file='/home/siiken/learning/tkinter/icons8-walter-white-50.png')
# root.iconphoto(True, icon)
root.geometry("600x800")
#Set the resizable property False
root.resizable(False, False)
# setting background image
bg_img = Image.open('images/pexels-emre-can-acer-2079451.jpg')
[imgSizeWidth, imgSizeHeight] = bg_img.size
bg_img = bg_img.resize((int(imgSizeWidth*0.20), int(imgSizeHeight*0.20)))
bg_img = ImageTk.PhotoImage(bg_img)
canvasMain = Canvas(root)
canvasMain.create_image(-50, -200, image=bg_img, anchor=NW)
canvasMain.place(x=0, y=0, relwidth=1, relheight=1)


def open_db():
    root.filename = filedialog.askopenfilename(
                                    initialdir="db/",
                                    title="Select a file:",
                                    filetypes=(("database files", "*.db"),)
                                    )
    # Create a database or connect to connect
    conn = sqlite3.connect(root.filename)

    # Close connection
    conn.close()


def create_db():
    def create_db_ok():
        # Create a database
        conn = sqlite3.connect(f'db/{create_db_entry.get()}.db')
        # Create cursor
        c = conn.cursor()

        # Commit changes
        conn.commit()

        # Close connection
        conn.close()
        # Create new windows to set new database name
        create_db_win.destroy()

    create_db_win = Toplevel(root)
    create_db_win.geometry("400x200")
    create_db_win.title("Create new database")

    create_db_label = Label(create_db_win, text="Set a name for your new database:")
    create_db_label.grid(row=0, columnspan=2, padx=5)
    create_db_entry = Entry(create_db_win)
    create_db_entry.grid(row=1, columnspan=2, padx=5)
    create_db_btn = Button(create_db_win, text="Create database", command=create_db_ok)
    create_db_btn.grid(row=2, column=0, padx=5)
    create_db_exit = Button(create_db_win, text="Back", command=create_db_win.destroy)
    create_db_exit.grid(row=2, column=1, padx=5)


open_db_btn = Button(root, text="Open database", padx=40, pady=30, command=open_db, fg="white", bg="black")
open_db_btn.pack(pady=(50, 0))

create_db_btn = Button(root, text="Create database", padx=35, pady=30, command=create_db, fg="white", bg="black")
create_db_btn.pack(pady=(50, 0))

exit_btn = Button(root, text="Exit", padx=40, pady=30, command=root.quit, fg="white", bg="black")
exit_btn.pack(pady=(50, 0))

'''
# Create a database or connect to connect
conn = sqlite3.connect('address_book.db')
# Create cursor
c = conn.cursor()

# Commit changes
conn.commit()

# Close connection
conn.close()
'''


root.mainloop()