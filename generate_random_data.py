import click
import json

from faker import Faker


cupcake_list = ['sesame', 'snaps', 'bonbon', 'tiramisu', 'croissant', 'croissant', 'biscuit', 'dessert', 'caramels', 'dragée', 'cookie', 'cupcake', 'cake', 'toffee', 'love', 'sweet', 'chocolate', 'halvah', 'love', 'icing', 'chocolate', 'toffee', 'chocolate', 'cake', 'jujubes', 'sweet', 'marshmallow', 'toffee', 'bear', 'claw']


def generate_author():
    return Faker().name()


def generate_book():
    return Faker().sentence(ext_word_list=cupcake_list, nb_words=3).replace('.', '')


@click.command()
@click.argument('number')
def main(number):
    json_dict = {"books": []}
    for i in range(int(number)):
        json_dict['books'].append({"book": generate_book(), "author": generate_author()})
    with open('authors_and_books.json', 'w') as fp:
        json.dump(json_dict, fp)

if __name__ == '__main__':
    main()