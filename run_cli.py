import click
from no_idea_how_to_name_this import db


@click.command()
@click.argument('args', nargs=-1)
def main(args):
    action, dbname = args[:2]
    username = args[-1] if len(args) == 3 else None
    if action == 'create':
        db.create_table(dbname)
    elif action == 'update':
        db.add_user(dbname, username)
    elif action == 'delete':
        db.delete_user(dbname, username)
    else:
        print('Didn\'t recognize the command "{}"'.format(action))


if __name__ == '__main__':
    main()