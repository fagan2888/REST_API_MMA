'''
Auto-discoverable by pytest when named test_*.py.
Command is `python -m pytest -v`.
'''
import pytest  # type: ignore
import base64

import utils
import pdb


def test_index_no_credentials(client, auth):
    response = client.get('/')

    assert response.status_code == 401


def test_index_with_credentials(client, auth):
    creds = base64.b64encode(b'testuser@mail.com:pass123').decode('utf-8')
    response = client.get('/', headers={'Authorization': 'Basic ' + creds})

    assert response.status_code == 200


@pytest.mark.static
def test_get_event_list(static_soup):
    json_response = utils.get_event_list(static_soup)

    assert json_response == {
        'Bellator 233: Salter vs. van Steenis': 'November 8th',
        'Combate 49: San Antonio': 'November 8th',
        'UFC on ESPN+ 21: Zabit vs. Kattar': 'November 9th',
        'UFC on ESPN+ 22: Blachowicz vs. Jacare': 'November 16th',
        'Combate: Hildago': 'December 7th',
        'UFC 245: Usman vs. Covington': 'December 14th',
        'UFC on ESPN+ 23: Ortega vs. The Korean Zombie': 'December 21st',
    }


@pytest.mark.static
def test_odds_makers_list(static_soup):
    json_response = utils.get_odds_makers_list(static_soup)

    assert json_response == [
        '5Dimes',
        'Bet365',
        'BetDSI',
        'BetOnline',
        'BookMaker',
        'Bovada',
        'Intertops',
        'Pinnacle',
        'SportBet',
        'SportsInt.',
        'Sportsbook',
        'TheGreek',
        'William\xa0H.',
    ]


@pytest.mark.static
def test_get_fighter_list(static_soup):
    json_response = utils.get_fighter_list('1', static_soup)

    assert json_response == {
        'Bellator 233: Salter vs. van Steenis': [
            'Costello Van Steenis',
            'John Salter',
            'Andrew Kapel',
            'Muhammed Lawal',
        ]
    }


@pytest.mark.static
def test_get_fighter_odds(static_soup):
    json_response = utils.get_fighter_odds('colby+covington', static_soup)

    assert json_response == {
        'odds': {
            '5Dimes': '+145',
            'Bet365': '',
            'BetDSI': '+139',
            'BetOnline': '+148',
            'BookMaker': '+140',
            'Bovada': '+140',
            'Intertops': '+115',
            'Pinnacle': '+130',
            'SportBet': '+145',
            'SportsInt.': '+130',
            'Sportsbook': '+145',
            'TheGreek': '+130',
            'William\u00a0H.': '',
        },
        'opponent': 'Kamaru Usman',
    }


def test_get_num_events(static_soup):
    num_events = utils.get_num_events(static_soup)

    assert num_events == 7
