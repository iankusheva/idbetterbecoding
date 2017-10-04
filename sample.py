import click
import os
import sqlite3


@click.command()
@click.option('--dbname', prompt='Enter database name')
def manipulate_tables(dbname):
    running_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_db = os.path.join(running_dir, '{}.db'.format(dbname))
    if os.path.exists(path_to_db):
        print('Database {}.db already exists'.format(dbname))
        return
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE table1 ('
                   'userid integer PRIMARY KEY, username text)')


def main():
    manipulate_tables()


if __name__ == '__main__':
    main()