'''
conftest.py stores pytest fixtures that can be used by all test files.
'''

from flask import Flask
import json 
from bs4 import BeautifulSoup
import pytest
import os

import main

## if running in parent directory, need to append folder path `tests` ##
if os.getcwd().endswith('tests'):
	html_fname = 'test_page.html'
else:
	html_fname = 'tests/test_page.html'	

@pytest.fixture()
def client(request):
    test_client = main.app.test_client()

    def teardown():
        pass # databases and resourses have to be freed at the end. But so far we don't have anything

    request.addfinalizer(teardown)
    return test_client

@pytest.fixture()
def static_soup(client):
	'''
	HTML page is constantly updated with new informtion. 
	Cache static page to test functionality.
	'''
	html = open(html_fname, 'r', encoding='utf-8').read()
	soup = BeautifulSoup(html, 'html.parser')	

	return soup