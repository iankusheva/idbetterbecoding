import os
import sqlite3


def get_full_path_to_db(dbname):
    running_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(running_dir, '{}'.format(dbname))


def print_all_tables(dbname):
    path_to_db = get_full_path_to_db(dbname)
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    print(cursor.execute('SELECT * FROM table_users').fetchall())
    print(cursor.execute('SELECT * FROM table_books').fetchall())
    print(cursor.execute('SELECT * FROM table_authors').fetchall())
    print(cursor.execute('SELECT * FROM table_userbooks').fetchall())


def add_user(dbname, username):
    path_to_db = get_full_path_to_db(dbname)
    if not os.path.exists(path_to_db):
        print('Database {}.db does not exist, can\'t update'.format(dbname))
        return
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO table1 VALUES (NULL, ?)", (username,))
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
    if cursor.execute('SELECT * FROM table1 WHERE username=?', (username,)).fetchone():
        cursor.execute("DELETE FROM table1 WHERE username = ?", (username,))
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


def create_tables_in_db(path_to_db):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE table_users (userid integer PRIMARY KEY AUTOINCREMENT NOT NULL, username text NOT NULL UNIQUE)')
    cursor.execute('CREATE TABLE table_authors (authorid integer PRIMARY KEY AUTOINCREMENT NOT NULL, authorname text NOT NULL UNIQUE)')
    cursor.execute('CREATE TABLE table_books (bookid integer PRIMARY KEY AUTOINCREMENT NOT NULL, bookname text NOT NULL UNIQUE, authorid integer NOT NULL, FOREIGN KEY (authorid) REFERENCES table_authors(authorid))')
    cursor.execute('CREATE TABLE table_userbooks (userid integer NOT NULL, bookid integer NOT NULL, FOREIGN KEY (userid) REFERENCES table_users(userid), FOREIGN KEY (bookid) REFERENCES table_books(bookid))')


def upload_json_into_db(parsed_string, dbname):
    path_to_db = get_full_path_to_db(dbname)
    if not os.path.exists(path_to_db):
        create_tables_in_db(path_to_db)

    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    bookname = parsed_string['book']
    author = parsed_string['author']
    # print_all_tables()
    if cursor.execute("SELECT bookname from table_books WHERE bookname=?", (bookname, )).fetchall():
        return
    cursor.execute("INSERT OR IGNORE INTO table_authors VALUES (NULL, ?)", (author,))
    author_id = cursor.execute("SELECT authorid from table_authors WHERE authorname=?", (author, )).fetchone()[0]
    cursor.execute("INSERT INTO table_books VALUES (NULL, ?, ?)", (bookname, author_id))

    conn.commit()
    print_all_tables(dbname)
    print(author_id)