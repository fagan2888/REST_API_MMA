'''
conftest.py stores pytest fixtures that can be used by all test files.

scope='session' --> all functions share one setup and teardown call
scope='function' --> runs once per function
'''
from bs4 import BeautifulSoup  # type: ignore
import pytest  # type: ignore
import os

import app


@pytest.fixture(scope='session')
def client(request):
    test_client = app.app.test_client()

    return test_client


@pytest.fixture(scope='session')
def static_soup(client):
    '''
    HTML page is constantly updated with new informtion.
    Cache static page to test functionality.
    '''
    html = open(os.path.join('tests', 'test_page.html'),
        'r',
        encoding='utf-8').read()
    soup = BeautifulSoup(html, 'html.parser')

    return soup
