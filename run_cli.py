import click
import json
from dp_app import db


@click.group()
def cli():
    pass


@cli.command('create')
@click.argument('dbname')
def create_db(dbname):
    db.create_table(dbname)


@cli.command('add')
@click.argument('dbname')
@click.argument('username')
def add_user_to_db(dbname, username):
    db.add_user(dbname, username)


@cli.command('delete')
@click.argument('dbname')
@click.argument('username')
def delete_user_from_db(dbname, username):
    db.delete_user(dbname, username)


@cli.command('add_book')
@click.option('--json_file', default='json_string_books_only.txt')
@click.option('--dbname', default='favourite_books.db')
def upload_books_into_db(json_file, dbname):
    json_string = open(db.get_full_path_to_file(json_file)).read()
    parsed_json = json.loads(json_string)
    path_to_db = db.get_full_path_to_file(dbname)

    with db.DatabaseConnection(path_to_db=path_to_db) as conn:
        cursor = conn.cursor()
        for book in parsed_json['books']:
            bookname = book['book']
            author = book['author']
            db.upload_book_into_db(bookname, author, path_to_db, conn, cursor)


@cli.command('add_user_with_books')
@click.option('--json_file', default='json_string_users_with_books.txt')
@click.option('--dbname', default='favourite_books.db')
def upload_user_with_books_into_db(json_file, dbname):
    json_string = open(db.get_full_path_to_file(json_file)).read()
    parsed_json = json.loads(json_string)
    path_to_db = db.get_full_path_to_file(dbname)
    list_of_users = parsed_json['users']

    with db.DatabaseConnection(path_to_db=path_to_db) as conn:
        cursor = conn.cursor()
        for user in list_of_users:
            db.upload_user_into_db(user, path_to_db, conn, cursor)


if __name__ == '__main__':
    cli()