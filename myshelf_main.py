from tkinter import *
from PIL import ImageTk, Image


class OpenShelf:
    def __init__(self, db):
        self.db = db
        self.shelf = Toplevel()
        self.container = Frame(self.shelf)
        self.info_frame = Frame(self.shelf, height=2)

    def set_window(self):
        self.shelf.title("My shelf")
        self.shelf.geometry("600x800")
        # Set the resizable window property False
        self.shelf.resizable(False, False)
        # setting info frame at the bottom of the page with the name of the opened database
        info_bar = Label(self.info_frame,
                         text=self.db,
                         bd=1,
                         relief=SUNKEN,
                         anchor=E)
        self.container.pack(side="top", expand=TRUE, fill=BOTH)
        info_bar.grid(row=2, column=0, columnspan=3, sticky=W + E)
        self.info_frame.pack(side=BOTTOM, anchor="e", padx=8, pady=8)

    def open_my_shelf(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        # setting background image
        global bg_img
        bg_img = Image.open('images/pexels-emre-can-acer-2079451.jpg')
        [img_width, img_height] = bg_img.size
        bg_img = bg_img.resize((int(img_width * 0.20), int(img_height * 0.20)))
        bg_img = ImageTk.PhotoImage(bg_img)
        # place image in the background
        canvas = Canvas(self.container)
        canvas.create_image(-50, -200, image=bg_img, anchor=NW)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Main page buttons
        view_items_btn = Button(self.container, text="Show library", padx=40, pady=30,
                                command=self.view_items, fg="white", bg="black")
        view_items_btn.pack(pady=(70, 0))
        add_item_btn = Button(self.container, text="Add new item to library", padx=35, pady=30, fg="white", bg="black")
        add_item_btn.pack(pady=(70, 0))
        previous_window_btn = Button(self.container, text="Back", padx=40, pady=30,
                                     command=self.shelf.destroy, fg="white", bg="black")
        previous_window_btn.pack(pady=(70, 0))

    def view_items(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        # setting background image
        global bg_img
        bg_img = Image.open('images/pexels-emre-can-acer-2079451.jpg')
        [img_width, img_height] = bg_img.size
        bg_img = bg_img.resize((int(img_width * 0.20), int(img_height * 0.20)))
        bg_img = ImageTk.PhotoImage(bg_img)
        # place image in the background
        canvas = Canvas(self.container)
        canvas.create_image(-50, -200, image=bg_img, anchor=NW)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # item_list = Frame(container)
        previous_window_btn = Button(self.container, text="Back", padx=40, pady=30,
                                     command=self.open_my_shelf, fg="white", bg="black")
        previous_window_btn.pack(pady=(70, 0))
        # item_list.pack(fill=BOTH)
