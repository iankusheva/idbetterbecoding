import os
import sqlite3


class DatabaseConnection:

    def __init__(self, path_to_db):
        self.path_to_db = path_to_db
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path_to_db)
        create_tables_in_db(self.conn)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except:
            pass


def get_full_path_to_file(dbname):
    running_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(running_dir, dbname)


def print_all_tables(path_to_db, conn):
    for table in ('table_users', 'table_books', 'table_authors', 'table_userbooks'):
        print(table, '-' , conn.execute('SELECT * FROM {}'.format(table)).fetchall(), '\n')


def create_tables_in_db(conn):
    with open('/home/irina/Documents/pythonic_stuff/idbetterbecoding/dp_app/create_empty_tables_query.txt') as file_:
        conn.executescript(file_.read())


def upload_book_into_db(bookname, author, path_to_db, conn):
    # skip the rest if the book already exists
    if conn.execute("SELECT bookname from table_books WHERE bookname=?", (bookname, )).fetchall():
        return

    # add author, keep id
    conn.execute("INSERT OR IGNORE INTO table_authors (authorname) VALUES (?)", (author,))
    author_id = conn.execute("SELECT authorid from table_authors WHERE authorname=?", (author, )).fetchone()[0]

    # add book with a link to its author
    conn.execute("INSERT OR IGNORE INTO table_books (bookname, authorid) VALUES (?, ?)", (bookname, author_id))

    conn.commit()


def upload_user_into_db(user, path_to_db, conn):
    username = user["username"]

    conn.execute("INSERT OR IGNORE INTO table_users (username) VALUES (?)", (username,))
    user_id = conn.execute("SELECT userid from table_users WHERE username=?", (username,)).fetchone()[0]

    for book in user['favourites']:
        bookname = book['book']
        author = book['author']

        if not conn.execute("SELECT bookname from table_books WHERE bookname=?", (bookname,)).fetchall():
            upload_book_into_db(bookname, author, path_to_db, conn)
        book_id = conn.execute("SELECT bookid from table_books WHERE bookname=?", (bookname,)).fetchone()[0]

        if not conn.execute("SELECT * from table_userbooks WHERE userid=? AND bookid=?", (user_id, book_id)).fetchall():
            conn.execute("INSERT OR IGNORE INTO table_userbooks VALUES (?, ?)", (user_id, book_id))

    conn.commit()
