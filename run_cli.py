import click
import json
import jsonschema
from dp_app import db


def validate_json(json_file, json_schema):
    with open(db.get_full_path_to_file(json_file)) as a, open(db.get_full_path_to_file(json_schema)) as b:
        string_to_parse = a.read()
        schema = b.read()
        try:
            json_loaded = json.loads(string_to_parse)
            jsonschema.validate(json_loaded, json.loads(schema))
            return json_loaded
        except jsonschema.ValidationError as e:
            print(e.message)
        except jsonschema.SchemaError as e:
            print(e)


@click.group()
def cli():
    pass


@cli.command('add_book')
@click.option('--json_file', default='json_string_books_only.txt')
@click.option('--dbname', default='favourite_books.db')
def upload_books_into_db(json_file, dbname):
    parsed_json = validate_json(json_file, 'books_only_schema.json')
    path_to_db = db.get_full_path_to_file(dbname)

    with db.DatabaseConnection(path_to_db=path_to_db) as conn:
        for book in parsed_json['books']:
            bookname = book['book']
            author = book['author']
            db.upload_book_into_db(bookname, author, path_to_db, conn)
        db.print_all_tables(path_to_db, conn)


@cli.command('add_users_with_books')
@click.option('--json_file', default='json_string_users_with_books.txt')
@click.option('--dbname', default='favourite_books.db')
def upload_user_with_books_into_db(json_file, dbname):
    parsed_json = validate_json(json_file, 'users_with_books_schema.json')
    path_to_db = db.get_full_path_to_file(dbname)
    list_of_users = parsed_json['users']

    with db.DatabaseConnection(path_to_db=path_to_db) as conn:
        for user in list_of_users:
            db.upload_user_into_db(user, path_to_db, conn)
        db.print_all_tables(path_to_db, conn)


if __name__ == '__main__':
    cli()