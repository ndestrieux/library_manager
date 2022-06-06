import sqlite3
from tkinter import messagebox


def create_command(conn):
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
