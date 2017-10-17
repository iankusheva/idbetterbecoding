import os
import sqlite3


def get_full_path_to_db(dbname):
    running_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(running_dir, '{}.db'.format(dbname))


def add_user(dbname, username):
    path_to_db = get_full_path_to_db(dbname)
    if not os.path.exists(path_to_db):
        print('Database {}.db does not exist, can\'t update'.format(dbname))
        return
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO table1 VALUES (NULL, '{}')".format(username))
    conn.commit()
    print('Added username "{}" into {}.db'.format(username, dbname))
    # print(cursor.execute('SELECT * FROM table1').fetchall())


def delete_user(dbname, username):
    path_to_db = get_full_path_to_db(dbname)
    if not os.path.exists(path_to_db):
        print('Database {}.db does not exist, nothing to delete'.format(dbname))
        return
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    if cursor.execute('SELECT * FROM table1 WHERE username="{}"'.format(username)).fetchone():
        cursor.execute("DELETE FROM table1 WHERE username = '{}'".format(username))
        conn.commit()
        print('Deleted username "{}" from {}.db'.format(username, dbname))
    else:
        print('No username {} in database {}, nothing to delete'.format(username, dbname))


def create_table(dbname):
    path_to_db = get_full_path_to_db(dbname)
    if os.path.exists(path_to_db):
        print('Database {}.db already exists'.format(dbname))
        return
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE table1 ('
                   'userid integer PRIMARY KEY, username text UNIQUE)')
    return dbname


def upload_json_into_db(parsed_string):
    conn = sqlite3.connect('smart.db')
    cursor = conn.cursor()
    for elem in parsed_string['books']:
        bookname = elem['bookname']
        author = elem['authorname']
        cursor.execute("INSERT OR IGNORE INTO table_authors VALUES (NULL, ?)", (author,))