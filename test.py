import json
from unittest import TestCase, mock

from main import (
    categorize_product,
    find_number_of_words,
    get_products,
    get_word_lists,
)


class MockResponse(object):
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code


def mock_requests_get(*args, **kwargs):
    content = b'colour\ncolor\n'
    status_code = 200

    return MockResponse(content, status_code)


def mock_requests_post(*args, **kwargs):
    content = json.dumps({
        'data': {
            'products': [
                {
                    'id': 1,
                    'name': 'Name',
                    'description': 'Description',
                }
            ]
        }
    })
    status_code = 200

    return MockResponse(content, status_code)


class TestCategorizeProduct(TestCase):
    def test_is_american(self):
        self.assertEqual(categorize_product(1, 0), 'American English')

    def test_is_british(self):
        self.assertEqual(categorize_product(0, 11), 'British English')

    def test_is_mixed(self):
        self.assertEqual(
            categorize_product(5, 17),
            'Mixed British and American English',
        )

    def test_is_unknown(self):
        self.assertEqual(categorize_product(0, 0), 'Unknown')


class TestFindNumberOfWords(TestCase):
    def test_case_insenitivity(self):
        number_of_words = find_number_of_words(
            name='I have some words',
            description='i too have Some Words, and they are good.',
            word_list=['i', 'Have', 'some', 'Words'],
        )

        self.assertEqual(number_of_words, 8)


class TestGetProducts(TestCase):
    @mock.patch('requests.post', side_effect=mock_requests_post)
    def test_get_products(self, mock):
        file = ['234325\n']
        products = get_products(file)

        expected_products = [
            {
                'id': 1,
                'name': 'Name',
                'description': 'Description',
            }
        ]
        self.assertEqual(products, expected_products)


class TestGetWordLists(TestCase):
    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_get_word_lists(self, mock):
        american_words, british_words = get_word_lists()

        expected_words = ['colour', 'color']
        self.assertListEqual(american_words, expected_words)
        self.assertListEqual(british_words, expected_words)
