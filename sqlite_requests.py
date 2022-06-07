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


