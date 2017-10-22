import os
import sqlite3

from contextlib import contextmanager


# class realization of db connection cntx mngr
class DatabaseConnection():

    def __init__(self, path_to_db):
        self.path_to_db = path_to_db

    def __enter__(self):
        if not os.path.exists(self.path_to_db):
            self.conn = sqlite3.connect(self.path_to_db)
            create_tables_in_db(self.conn)
        else:
            self.conn = sqlite3.connect(self.path_to_db)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


# method with decorator realization
@contextmanager
def connect_to_db(path_to_db):
    if not os.path.exists(path_to_db):
        conn = sqlite3.connect(path_to_db)
        create_tables_in_db(conn)
    else:
        conn = sqlite3.connect(path_to_db)
    yield conn
    conn.close()


def get_full_path_to_file(dbname):
    running_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(running_dir, '{}'.format(dbname))


def print_all_tables(path_to_db, conn):
    cursor = conn.cursor()
    for table in ('table_users', 'table_books', 'table_authors', 'table_userbooks'):
        print(table, '-' , cursor.execute('SELECT * FROM {}'.format(table)).fetchall(), '\n')


def create_tables_in_db(conn):
    cursor = conn.cursor()
    with open('/home/irina/Documents/pythonic_stuff/idbetterbecoding/dp_app/create_empty_tables_query.txt') as file_:
        for command in file_.readlines():
            cursor.execute(command)


def upload_book_into_db(bookname, author, path_to_db, conn, cursor):
    # skip the rest if the book already exists
    if cursor.execute("SELECT bookname from table_books WHERE bookname=?", (bookname, )).fetchall():
        return

    # add author, keep id
    cursor.execute("INSERT OR IGNORE INTO table_authors (authorname) VALUES (?)", (author,))
    author_id = cursor.execute("SELECT authorid from table_authors WHERE authorname=?", (author, )).fetchone()[0]

    # add book with a link to its author
    cursor.execute("INSERT OR IGNORE INTO table_books (bookname, authorid) VALUES (?, ?)", (bookname, author_id))

    conn.commit()
    print_all_tables(path_to_db, conn)


def upload_user_into_db(user, path_to_db, conn, cursor):
    username = list(user.keys())[0]

    cursor.execute("INSERT OR IGNORE INTO table_users (username) VALUES (?)", (username,))
    user_id = cursor.execute("SELECT userid from table_users WHERE username=?", (username,)).fetchone()[0]

    for book in user[username]['favourites']:
        bookname = book['book']
        author = book['author']

        if not cursor.execute("SELECT bookname from table_books WHERE bookname=?", (bookname,)).fetchall():
            upload_book_into_db(bookname, author, path_to_db, conn, cursor)
        book_id = cursor.execute("SELECT bookid from table_books WHERE bookname=?", (bookname,)).fetchone()[0]

        if not cursor.execute("SELECT * from table_userbooks WHERE userid=? AND bookid=?", (user_id, book_id)).fetchall():
            cursor.execute("INSERT OR IGNORE INTO table_userbooks VALUES (?, ?)", (user_id, book_id))

    conn.commit()
    print_all_tables(path_to_db, conn)
