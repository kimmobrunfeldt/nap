.PHONY: help clean clean-pyc clean-build list test test-all coverage docs release sdist

help:
	@echo "clean - execute all clean tasks"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-coverage - remove coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "release - package and upload a release. This makes a patch release by default"
	@echo "          you can give bump parameter, valid values: patch, minor, major"
	@echo "          for example: make release bump=minor"
	@echo "pypi - release current code to PyPi. Remember to checkout a tag first."
	@echo "dist - package"

clean: clean-build clean-pyc clean-coverage

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-coverage:
	rm -f .coverage

lint:
	flake8 --exclude=__init__.py nap test

test: test-examples
	py.test

test-examples:
	egtest README.md

test-all:
	tox

coverage:
	coverage run --branch --source nap -m pytest
	coverage report -m

release: clean coverage test-all
	python scripts/make-release.py $(bump)

pypi: clean coverage test-all
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
