import click
import json
from dp_app import db


json_string_global = """
{
	"users": [{
		"vasya": {
			"favourites": [{
				"book": "Harry Potter and the Prisoner of Azkaban",
				"author": "J. K. Rowling"
			},
			{
				"book": "Harry Potter and the Deathly Hallows",
				"author": "J. K. Rowling"
			},
			{
				"book": "Harry Potter and the Half-Blood Prince",
				"author": "J. K. Rowling"
			}]
		}
	}, {
		"petya": {
			"favourites": [{
				"book": "The Lord of the Rings",
				"author": "J. R. R. Tolkien"
			},{
				"book": "Three Men in a Boat",
				"author": "Jerome K. Jerome"
			},{
				"book": "Ham on Rye",
				"author": "Charles Bukowski"
			}]
		}
	}, {
		"vasilisa": {
			"favourites": [{
				"book": "Harry Potter and the Prisoner of Azkaban",
				"author": "J. K. Rowling"
			},{
				"book": "The Martian Chronicles",
				"author": "Ray Bradbury"
			},{
				"book": "A Scandal in Bohemia",
				"author": "Arthur Conan Doyle"
			}]
		}
	}, {
		"sashka": {
			"favourites": [{
				"book": "A Scandal in Bohemia",
				"author": "Arthur Conan Doyle"
			},{
				"book": "The Adventure of the Yellow Face",
				"author": "Arthur Conan Doyle"
			},{
				"book": "The Adventure of the Final Problem",
				"author": "Arthur Conan Doyle"
			},{
				"book": "The Poison Belt",
				"author": "Arthur Conan Doyle"
			},{
				"book": "Ham on Rye",
				"author": "Charles Bukowski"
			}]
		}
	}, {
		"gregory": {
			"favourites": [{
				"book": "The Lord of the Rings",
				"author": "J. R. R. Tolkien"
			},{
				"book": "Harry Potter and the Prisoner of Azkaban",
				"author": "J. K. Rowling"
			},{
				"book": "Ham on Rye",
				"author": "Charles Bukowski"
			}]
		}
	}, {
		"solnyshko35": {
			"favourites": []
		}
	}]
}
"""

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
@click.argument('json_string')
@click.option('--dbname', default='favourite_books.db')
def upload_books_into_db(json_string, dbname):
    parsed_json = json.loads(json_string)
    path_to_db = db.get_full_path_to_db(dbname)

    with db.DatabaseConnection(path_to_db=path_to_db) as conn:
        cursor = conn.cursor()
        for book in parsed_json['books']:
            bookname = book['book']
            author = book['author']
            db.upload_book_into_db(bookname, author, path_to_db, conn, cursor)


@cli.command('add_user_with_books')
@click.argument('json_string')
@click.option('--dbname', default='favourite_books.db')
def upload_user_with_books_into_db(json_string, dbname):
    parsed_json = json.loads(json_string)
    path_to_db = db.get_full_path_to_db(dbname)
    list_of_users = parsed_json['users']

    with db.DatabaseConnection(path_to_db=path_to_db) as conn:
        cursor = conn.cursor()
        for user in list_of_users:
            db.upload_user_into_db(user, path_to_db, conn, cursor)


if __name__ == '__main__':
    cli()