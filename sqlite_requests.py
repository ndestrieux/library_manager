import sqlite3
from tkinter import *
from tkinter import messagebox
import re


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
        c.execute(f"SELECT *, rowid FROM {table_name} ORDER BY {order_by}")
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

    except sqlite3.OperationalError:
        messagebox.showerror("Error", "Database is not reachable please try again later.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Check your values, field 'Year' must be a number")

    else:
        # success message
        messagebox.showinfo("Info", "New item added to database")
        # reset form
        for e in entry_list:
            if type(e) is type(Entry()):
                e.delete(0, END)
            elif type(e) is type(IntVar()):
                e.set(0000)
            elif type(e) is type(Text()):
                e.delete('1.0', END)


def delete_entry(db, table, tree, row_count_label):
    selected = tree.selection()
    # If item(s) selected do the following
    if selected:
        item_list_to_delete = ""
        for s in selected:
            item_list_to_delete = f"{item_list_to_delete}{tree.item(s)['values'][0]}\n"
        confirmation = messagebox.askokcancel("Confirmation",
                                              f"Are your sure you want to delete the following items:\n"
                                              f"{item_list_to_delete}")
        # Get confirmation is data must be deleted
        if confirmation:
            # Check if database is reachable otherwise throw a message box with error
            try:
                conn = sqlite3.connect(f"file:{db}?mode=rw", uri=True)
                c = conn.cursor()
            except sqlite3.OperationalError:
                messagebox.showerror("Error", "Database is not reachable please try again later.")
            else:
                # Delete row(s) selected from database and on the list displayed
                for s in selected:
                    c.execute(f"DELETE FROM {table} WHERE rowid = {s}")
                    tree.delete(s)

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                # Update row count
                old_row_count = int(re.search("\d+", row_count_label["text"]).group(0))
                new_row_count = old_row_count - len(selected)
                row_count_label["text"] = re.sub("\d+", str(new_row_count),
                                                 row_count_label["text"]
                                                 if new_row_count > 1 else row_count_label["text"][:-1])

                # Confirmation that the data was deleted
                messagebox.showinfo("Info", f"The following items have been deleted:\n{item_list_to_delete}")
