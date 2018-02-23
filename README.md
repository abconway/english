# english
A command line tool for categorizing products by the flavor (flavour) of English used.

## Dependencies
- Python 3
- Virtualenv

## Quickstart
```
make
source venv/bin/activate
english parse_products --file <path_to_file_with_product_ids>
```
or
```
make
./venv/bin/english parse_products --file <path_to_file_with_product_ids>
```

## Developement and Testing
```
make develop
make test
```

## Discussion
The entry point of this tool is the 'parse_products' function 
in the main.py file.  The parse_products function takes
a command line argument file path pointing to a text file containing 
product_ids to be checked. The function first grabs updated
word list definitions from a github gist. The product_ids are then
read in and used to make a request to a graphql endpoint to
retrieve more information about the products. Each product's name
and description are parsed and checked against the word lists to
see how many words can be considered "American English" vs
"British English". Based on the numbers of words for each, the
product is categorized as either American English, British English,
Mixed British and American English, or Unknown. The product_ids
are printed to stdout with the determined categorization.

The text parsing is done with a case-insensitive regex.
It is unsophisticated and by no means robust.

A simple suite of tests can be found in the test.py file.

## Assumptions
The input file of product_ids is well formed with a single
product_id per line.

The word lists retrieved from the github gist are also
well formed with a single word per line.

The products endpoint is assumed to return json data in the
form of a dictionary (hash) with a top level key called 'data',
with a sub-key called 'products' that is a list of
products containing at minimum an id, name, and description.

A product is considered to be American English if at least
one word was found to be from list of American English words
and no words were found from the list of British English words.

A product is considered to be British English if at least
one word was found to be from list of British English words
and no words were found from the list of American English words.

A product is considered to be Mixed British and American 
English if at least one word was found to be from list of 
American English words and at least one word was found from 
the list of British English words.

A product is considered to be Unknown if no words were found from
either the American or British list of words.