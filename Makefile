.PHONY: all

all: clean venv install

clean:
	rm -rf venv

develop: install
	venv/bin/pip install -r requirements.txt

install:
	venv/bin/pip install -e .

venv:
	virtualenv venv -p $(shell which python3)
