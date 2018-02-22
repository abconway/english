.PHONY: all test

all: install

clean:
	rm -rf venv

develop: install
	venv/bin/pip install -r requirements.txt

install: venv
	venv/bin/pip install -e .

test:
	./venv/bin/nosetests

venv: clean
	virtualenv venv -p $(shell which python3)
