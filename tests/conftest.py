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

class AuthActions(object):
    def __init__(self, client):
        self._client = client
        self.login()

    def login(self, username='testuser@mail.com', password='pass123'):
        password = app.bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
        return self._client.post(
            '/',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
