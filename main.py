import re
import json

import click
import requests


__version__ = '0.0.1'
AMERICAN_WORDS_URL = 'https://gist.githubusercontent.com/mdg/aa4c9070ff3dbeaa5d4613cba05c2faf/raw/c9f1795048a9d7f841079aca2a66f14ef3e7002b/american-words.txt'
BRITISH_WORDS_URL = 'https://gist.githubusercontent.com/mdg/aa4c9070ff3dbeaa5d4613cba05c2faf/raw/c9f1795048a9d7f841079aca2a66f14ef3e7002b/british-words.txt'
GRAPH_QL_URL = 'https://www.teacherspayteachers.com/graph/graphql'
GRAPH_QL_QUERY = '''
    query productText($productIds: [ID]!) {
        products(ids: $productIds) {
            id
            name
            description
        }
    }
'''


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command(help='Parse a file of product ids and categorize the type of English')
@click.option('--file', '-f', type=click.File(),
              help='File containing Product IDs')
def parse_products(file):
    american_words, british_words = get_word_lists()
    products = get_products(file=file)

    for product in products:
        id = product.get('id')
        name = product.get('name')
        description = product.get('description')

        american_word_count = find_number_of_words(
            name=name,
            description=description,
            word_list=american_words
        )

        british_word_count = find_number_of_words(
            name=name,
            description=description,
            word_list=british_words
        )

        category = categorize_product(american_word_count, british_word_count)

        print('Product ID: {} -> {}'.format(id, category))


def categorize_product(american_word_count, british_word_count):
    if american_word_count and not british_word_count:
        return 'American English'
    elif british_word_count and not american_word_count:
        return 'British English'
    elif american_word_count and british_word_count:
        return 'Mixed British and American English'
    return 'Unknown'


def find_number_of_words(name, description, word_list):
    word_count = 0

    words_to_find = '|'.join(word_list)
    pattern = r'({})'.format(words_to_find)

    word_count += len(re.findall(pattern, name, re.IGNORECASE))
    word_count += len(re.findall(pattern, description, re.IGNORECASE))

    return word_count


def get_products(file):
    product_ids = []
    for line in file:
        product_ids.append(line.strip())

    variables = json.dumps({"productIds": product_ids})
    data = {
        'query': GRAPH_QL_QUERY,
        'variables': variables
    }
    response = requests.post(GRAPH_QL_URL, data=data)

    if response.status_code != 200:
        raise Exception('Failed to get the products list.')

    return json.loads(response.content).get('data').get('products')


def get_word_lists():
    response = requests.get(AMERICAN_WORDS_URL)

    if response.status_code != 200:
        raise Exception('Failed to get the American Word list from github.')

    raw_american_words = response.content.decode("utf-8")
    american_words = raw_american_words.rstrip().split('\n')

    response = requests.get(BRITISH_WORDS_URL)

    if response.status_code != 200:
        raise Exception('Failed to get the British Word list from github.')

    raw_british_words = response.content.decode("utf-8")
    british_words = raw_british_words.rstrip().split('\n')

    return (american_words, british_words)
