import click
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


if __name__ == '__main__':
    cli()