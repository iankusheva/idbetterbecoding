import click
import os
import sqlite3


def get_full_path_to_db(dbname):
    running_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(running_dir, '{}.db'.format(dbname))


@click.command()
@click.option('--username', prompt='Enter a username to be added')
def add_user(username):
    dbname = 'pam'
    path_to_db = get_full_path_to_db(dbname)
    # if os.path.exists(path_to_db):
    #     print('Database {}.db already exists'.format(dbname))
    #     return
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    # select_max = cursor.execute("SELECT MAX(userid) FROM table1").fetchall()[0][0]
    # max_id = int(select_max) if select_max is not None else 0
    # print(max_id)
    cursor.execute("INSERT INTO table1 VALUES (NULL, '{}')".format(username))
    conn.commit()
    print(cursor.execute('SELECT * FROM table1').fetchall())


@click.command()
@click.option('--dbname', prompt='Enter database name')
@click.option('--username', prompt='Enter a username to be deleted')
def delete_user(dbname, username):
    path_to_db = get_full_path_to_db(dbname)
    if not os.path.exists(path_to_db):
        print('Database {}.db does not exist'.format(dbname))
        return
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM table1 WHERE username = '{}'".format(username))
    conn.commit()
    print(cursor.execute('SELECT * FROM table1').fetchall())


@click.command()
@click.option('--dbname', prompt='Enter database name')
def create_table(dbname):
    path_to_db = get_full_path_to_db(dbname)
    if os.path.exists(path_to_db):
        print('Database {}.db already exists'.format(dbname))
        return
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE table1 ('
                   'userid integer PRIMARY KEY, username text)')
    return dbname


@click.command()
@click.option('--action', prompt='Choose an action to perform (CUD)', type=click.Choice(['C', 'U', 'D']))
def do_stuff(action):
    if action == 'C':
        create_table()
    elif action == 'U':
        add_user()
    elif action == 'D':
        delete_user()


def main():
    do_stuff()


if __name__ == '__main__':
    main()