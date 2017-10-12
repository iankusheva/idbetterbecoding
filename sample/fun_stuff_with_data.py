import click
import sys
from sample import db


@click.command()
@click.option('--action', prompt='Choose an action to perform (CUD, or Q for quit)', type=click.Choice(['C', 'U', 'D', 'Q']))
def do_stuff(action):
    if action == 'C':
        db.create_table(standalone_mode=False)
    elif action == 'U':
        db.add_user(standalone_mode=False)
    elif action == 'D':
        db.delete_user(standalone_mode=False)
    elif action == 'Q':
        sys.exit(0)


def main():
    while True:
        do_stuff(standalone_mode=False)


if __name__ == '__main__':
    main()