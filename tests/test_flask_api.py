'''
Auto-discoverable by pytest when named test_*.py.
Command is `pytest -v`.

Functions besides test_connect and test_index pull dynamic data.
'''

from flask import Flask
import json
from bs4 import BeautifulSoup  # type: ignore
import pytest  # type: ignore

import utils

url = 'http://127.0.0.1:5000' # The root url of the flask app

def test_index(client):
    response = client.get('/')
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
	json_response = utils.odds_makers_list(static_soup)

	assert json_response == json.dumps(['5Dimes',
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
										'William\u00a0H.'])

# @pytest.mark.static
# def test_odds_makers_list_helper(static_soup):
# 	bettor_lst = main.odds_makers_list_helper(static_soup)

# 	assert bettor_lst == ['5Dimes',
# 						  'Bet365',
# 						  'BetDSI',
# 						  'BetOnline',
# 						  'BookMaker',
# 						  'Bovada',
# 						  'Intertops',
# 						  'Pinnacle',
# 						  'SportBet',
# 						  'SportsInt.',
# 						  'Sportsbook',
# 						  'TheGreek',
# 						  'William\u00a0H.']

# @pytest.mark.static
# def test_get_fighter_list(static_soup):
# 	json_response = main.get_fighter_list('1',static_soup)

# 	assert json_response == json.dumps({'Combate 49: San Antonio': ['Andre Barquero Morera',
# 																	'Eduardo Alvarado Osuna',
# 																	'Jason Norwood',
# 																	'Jose Caceres',
# 																	'Cesar Arzamendia',
# 																	'Fernando Gonzalez Trevino',
# 																	'Justin Governale',
# 																	'Peter Caballero',
# 																	'Chris Cortez',
# 																	'Oscar Suarez',
# 																	'Melissa Cervantes',
# 																	'Nadine Mandiau',
# 																	'Andy Perez',
# 																	'Ray Rodriguez',
# 																	'Carlos Melara',
# 																	'Roy Sarabia']})

# @pytest.mark.static
# def test_get_fighter_odds(static_soup):
# 	json_response = main.get_fighter_odds('colby+covington',static_soup)

# 	assert json_response == json.dumps({'odds': {'5Dimes': '+145',
# 												 'Bet365': '',
# 												 'BetDSI': '+139',
# 												 'BetOnline': '+148',
# 												 'BookMaker': '+140',
# 												 'Bovada': '+140',
# 												 'Intertops': '+115',
# 												 'Pinnacle': '+130',
# 												 'SportBet': '+145',
# 												 'SportsInt.': '+130',
# 												 'Sportsbook': '+145',
# 												 'TheGreek': '+130',
# 												 'William\u00a0H.': ''},
# 										'opponent': 'Kamaru Usman'})