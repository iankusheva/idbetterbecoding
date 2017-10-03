import click
import os
import sqlite3


def manipulate_tables(dbname):
    running_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(running_dir, '{}.db'.format(dbname))):
        print('Database {}.db already exists'.format(dbname))
        return
    conn = sqlite3.connect('{}.db'.format(dbname))
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE table1 ('
                   'userid integer PRIMARY KEY, username text)')


@click.command()
@click.option('--dbname', prompt='Enter database name')
def main(dbname):
    manipulate_tables(dbname)


if __name__ == '__main__':
    main()