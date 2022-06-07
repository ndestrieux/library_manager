import sqlite3


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


def fetch_data_from_database(db, table_name):
    conn = sqlite3.connect(db)
    c = conn.cursor()
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
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Set tables database columns
    if table == "books":
        columns = "(title, author, year, publisher)"
    elif table == "album":
        columns = "(title, artist_name, year, genre, format, cover)"
    elif table == "films":
        columns = "(title, year, film_info, cover)"

    entry_values = "("
    # Get value from entries
    for e in entry_list:
        if e != entry_list[-1]:
            entry_values = f"{entry_values}\'{e.get()}\', "
        else:
            entry_values = f"{entry_values}\'{e.get()}\')"

    c.execute(f"""
                INSERT INTO {table} {columns}
                VALUES {entry_values}
                """)
    # print(columns, entry_values)

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()




