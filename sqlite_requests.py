import sqlite3
from tkinter import *
from tkinter import messagebox
from constants import YEAR_OPTIONS


def create_command(new_db):
    # Connect to database
    conn = sqlite3.connect(new_db)

    # Create cursor
    c = conn.cursor()

    # Create table album
    c.execute("""
                CREATE TABLE "album" (
                "title"	TEXT NOT NULL,
                "artist_name"	TEXT NOT NULL,
                "year"	INTEGER
                CHECK(typeof(year) == 'integer'),
                "genre"	TEXT,
                "format"    TEXT)
                """)

    # Create table books
    c.execute("""
                CREATE TABLE "books" (
                "title"	TEXT NOT NULL,
                "author"	TEXT,
                "year"	INTEGER
                CHECK(typeof(year) == 'integer'),
                "publisher"	TEXT)
                """)

    # Create table films
    c.execute("""
                CREATE TABLE "films" (
                "title"	TEXT NOT NULL,
                "year"	INTEGER
                CHECK(typeof(year) == 'integer'),
                "film_info"	TEXT)
                """)

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()


def fetch_data_from_database(db, table_name):
    # Check if database is reachable otherwise throw a message box with error
    try:
        conn = sqlite3.connect(f"file:{db}?mode=rw", uri=True)
        c = conn.cursor()
    except sqlite3.OperationalError:
        messagebox.showerror("Error", "Database is not reachable please try again later.")
        return ()
    else:
        if table_name == "books":
            order_by = "author"
        elif table_name == "album":
            order_by = "artist_name"
        elif table_name == "films":
            order_by = "title"
        c.execute(f"SELECT * FROM {table_name} ORDER BY {order_by}")
        rows = c.fetchall()
        c.close()
        return rows


def save_item(db, table, entry_list):
    # Set tables database columns
    if table == "books":
        columns = ("title", "author", "year", "publisher")
    elif table == "album":
        columns = ("title", "artist_name", "year", "genre", "format")
    elif table == "films":
        columns = ("title", "year", "film_info")

    # Get value from entries and add it to a list
    entry_value_list = []
    for e in entry_list:
        entry_value_list.append(e.get() if type(e) is not type(Text()) else e.get('1.0', END))

    # Check if database is reachable or if the values are correct otherwise throw a message box with error
    try:
        conn = sqlite3.connect(f"file:{db}?mode=rw", uri=True)
        c = conn.cursor()

        # SQL request to add item in table
        query = f"INSERT INTO {table} {columns} VALUES ({'?, ' * (len(entry_value_list) - 1) + '?'})"
        c.execute(query, entry_value_list)

        # Commit changes
        conn.commit()

        # Close connection
        conn.close()

    except sqlite3.OperationalError as OE:
        messagebox.showerror("Error", "Database is not reachable please try again later.")
    except sqlite3.IntegrityError as IE:
        messagebox.showerror("Error", "Check your values, field 'Year' must be a number")

    else:
        # success message
        messagebox.showinfo("Info", f"New item added to database")
        # reset form
        for e in entry_list:
            if type(e) is type(Entry()):
                e.delete(0, END)
            elif type(e) is type(IntVar()):
                e.set((YEAR_OPTIONS[0]))
            elif type(e) is type(Text()):
                e.delete('1.0', END)
