from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from sqlite_requests import fetch_data_from_database as fd, save_item


class OpenShelf:
    def __init__(self, db):
        self.db = db
        self.shelf = Toplevel()
        self.container = Frame(self.shelf)
        self.info_frame = Frame(self.shelf, height=2)

    def set_window(self):
        self.shelf.title("My shelf")
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
        # Remove widgets previously set in this window
        for widget in self.container.winfo_children():
            widget.destroy()
        self.shelf.geometry("600x800")
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

        # Set grid for buttons
        self.container.columnconfigure((0, 1), weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.rowconfigure((0, 1, 2, 3), weight=1)

        # Main page buttons
        view_books_btn = Button(self.container, text="Show books", padx=28, pady=20,
                                command=lambda: self.view_items("books"), fg="white", bg="black")
        view_books_btn.grid(row=0, column=0)
        add_books_btn = Button(self.container, text="Add books", padx=28, pady=20,
                               command=lambda: self.add_item("books"), fg="white", bg="black")
        add_books_btn.grid(row=0, column=1)
        view_music_btn = Button(self.container, text="Show music", padx=28, pady=20,
                                command=lambda: self.view_items("album"), fg="white", bg="black")
        view_music_btn.grid(row=1, column=0)
        add_music_btn = Button(self.container, text="Add music", padx=28, pady=20,
                               command=lambda: self.add_item("album"), fg="white", bg="black")
        add_music_btn.grid(row=1, column=1)
        view_films_btn = Button(self.container, text="Show films", padx=31, pady=20,
                                command=lambda: self.view_items("films"), fg="white", bg="black")
        view_films_btn.grid(row=2, column=0)
        add_films_btn = Button(self.container, text="Add films", padx=31, pady=20,
                               command=lambda: self.add_item("films"), fg="white", bg="black")
        add_films_btn.grid(row=2, column=1)
        previous_window_btn = Button(self.container, text="Back", padx=28, pady=20,
                                     command=self.shelf.destroy, fg="white", bg="black")
        previous_window_btn.grid(row=3, rowspan=2, columnspan=2)

    # Display entries from database
    def view_items(self, table):
        # Remove widgets previously set in this window
        for widget in self.container.winfo_children():
            widget.destroy()
        # Set new window size
        self.shelf.geometry("1200x1000")
        # get data from the selected table
        rows = fd(self.db, table)
        # Set table for displaying books
        if table == "books":
            view_title = "My books"
            tree = ttk.Treeview(self.container,
                                column=("title", "author", "year", "publisher"), show='headings')
            tree.column("#1", anchor=CENTER)
            tree.heading("#1", text="Title")
            tree.column("#2", anchor=CENTER)
            tree.heading("#2", text="Author")
            tree.column("#3", anchor=CENTER)
            tree.heading("#3", text="Year")
            tree.column("#4", anchor=CENTER)
            tree.heading("#4", text="Publisher")
            item_name = "book"

        # Set table for displaying album
        elif table == "album":
            view_title = "My music"
            tree = ttk.Treeview(self.container,
                                column=("title", "artist_name", "year", "genre", "format"), show='headings')
            tree.column("#1", anchor=CENTER)
            tree.heading("#1", text="Title")
            tree.column("#2", anchor=CENTER)
            tree.heading("#2", text="Artist")
            tree.column("#3", anchor=CENTER)
            tree.heading("#3", text="Year")
            tree.column("#4", anchor=CENTER)
            tree.heading("#4", text="Genre")
            tree.column("#5", anchor=CENTER)
            tree.heading("#5", text="Format")
            item_name = "album"

        # Set table for displaying films
        elif table == "films":
            view_title = "My films"
            tree = ttk.Treeview(self.container,
                                column=("title", "year", "info"), show='headings')
            tree.column("#1", anchor=CENTER)
            tree.heading("#1", text="Title")
            tree.column("#2", anchor=CENTER)
            tree.heading("#2", text="Year")
            tree.column("#3", anchor=CENTER)
            tree.heading("#3", text="Info")
            item_name = "DVD"

        # Insert view title
        view_title_label = Label(self.container, text=view_title, font=("Arial", 25))
        view_title_label.pack()
        # Insert column headers
        tree.pack(side="top", expand=TRUE, fill=BOTH)
        # Insert rows in window from selected table
        for row in rows:
            tree.insert("", END, values=row)

        # display the number of items in the library as per the category selected
        plural = "s"
        row_count = len(rows)
        row_count_label = Label(self.container,
                                text=f"You have {row_count} {item_name}{plural if row_count > 1 else ''}")
        row_count_label.pack(anchor=E, padx=8)
        # Return to previous window
        previous_window_btn = Button(self.container, text="Back", padx=20, pady=15,
                                     command=self.open_my_shelf, fg="white", bg="black")
        previous_window_btn.pack(side=BOTTOM, anchor=W, padx=8, pady=4)

    def add_item(self, table):
        # Remove widgets previously set in this window
        for widget in self.container.winfo_children():
            widget.destroy()
        # Set new window size
        self.shelf.geometry("600x800")
        # setting background image

        # Set grid for the view
        self.container.columnconfigure((0, 1), weight=1)
        self.container.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        global bg_img
        bg_img = Image.open('images/pexels-emre-can-acer-2079451.jpg')
        [img_width, img_height] = bg_img.size
        bg_img = bg_img.resize((int(img_width * 0.20), int(img_height * 0.20)))
        bg_img = ImageTk.PhotoImage(bg_img)
        # place image in the background
        canvas = Canvas(self.container)
        canvas.create_image(-50, -200, image=bg_img, anchor=NW)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Set view title and label names as per the table selected
        if table == "books":
            label_list = ["Add book", "Title", "Author", "Year", "Publisher"]
        if table == "album":
            label_list = ["Add album", "Title", "Artist", "Year", "Genre", "Format"]
        if table == "films":
            label_list = ["Add film", "Title", "Year", "Info"]

        # Insert view title on window
        page_title = Label(self.container, text=label_list[0], font=("Arial", 28), bg="#DCB56E")
        page_title.grid(row=0, columnspan=2, sticky=W+N+E+S)
        # Unpack and display labels and entries
        entry_list = []
        row_nb = 1
        for label in label_list[1:]:
            label = Label(self.container, text=label, font=("Arial", 18), bg="#DCB56E")
            label.grid(row=row_nb, column=0, sticky=E, padx=10),
            entry = Text(self.container, height=3, width=40)
            entry.grid(row=row_nb, column=1)
            entry_list.append(entry)
            row_nb += 1

        # Go back to previous menu
        back_btn = Button(self.container, text="Back", padx=20, pady=15,
                          command=self.open_my_shelf, fg="white", bg="black")
        back_btn.grid(row=5, column=0, sticky=W, padx=8, pady=8)
        # Save new item
        save_btn = Button(self.container, text="Save", padx=20, pady=15,
                          command=lambda: save_item(self.db, table, entry_list), fg="white", bg="black")
        save_btn.grid(row=5, column=1, sticky=E, padx=8, pady=8)
