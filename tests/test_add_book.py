import os
import subprocess
import sqlite3
import json


PATH_TO_FOLDER = '/home/irina/Documents/pythonic_stuff/idbetterbecoding/'
DBNAME = 'test_add_book_db.db'


def setup():
    print("basic setup")


def teardown():
    path_to_db = os.path.join(PATH_TO_FOLDER, 'dp_app', DBNAME)
    print(path_to_db)
    if os.path.exists(path_to_db):
        os.remove(path_to_db)


def test_database():
    print("testing db")

    # run upload_books_into_db from run_cli
    cmd = "python3.5 {}run_cli.py add_book --json_file=authors_and_books.json --dbname={}".format(PATH_TO_FOLDER, DBNAME)
    subprocess.call(cmd, shell=True)

    # generate dict from db data
    conn = sqlite3.connect(os.path.join(PATH_TO_FOLDER, 'dp_app', DBNAME))
    authors = {author[0]: author[1] for author in conn.execute('SELECT * FROM table_authors').fetchall()}
    books = {book[2]: book[1] for book in conn.execute('SELECT * FROM table_books').fetchall()}
    db_dict = {"books": []}
    for key, book in books.items():
        db_dict["books"].append({"author": authors[key], "book": book})

    # compare db with original test json
    with open(os.path.join(PATH_TO_FOLDER, 'dp_app', 'authors_and_books.json')) as json_file:
        json_dict = json.loads(json_file.read())
    assert db_dict== json_dict