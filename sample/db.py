import click
import os
import sqlite3
import sys


def get_full_path_to_db(dbname):
    running_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(running_dir, '{}.db'.format(dbname))


@click.command()
@click.option('--dbname', prompt='Enter database name')
@click.option('--username', prompt='Enter a username to be added')
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


@click.command()
@click.option('--dbname', prompt='Enter database name')
@click.option('--username', prompt='Enter a username to be deleted')
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
@click.option('--action', prompt='Choose an action to perform (CUD, or Q for quit)', type=click.Choice(['C', 'U', 'D', 'Q']))
def do_stuff(action):
    if action == 'C':
        create_table(standalone_mode=False)
    elif action == 'U':
        add_user(standalone_mode=False)
    elif action == 'D':
        delete_user(standalone_mode=False)
    elif action == 'Q':
        sys.exit(0)


def main():
    while True:
        do_stuff(standalone_mode=False)


if __name__ == '__main__':
    main()