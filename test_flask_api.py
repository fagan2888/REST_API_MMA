'''
Auto-discoverable by pytest when named test_*.py.
Command is `pytest -v`.

Functions besides test_connect and test_index pull dynamic data.
'''

import requests
from flask import Flask
import os
import json 
from bs4 import BeautifulSoup
import pytest

import main

url = 'http://127.0.0.1:5000' # The root url of the flask app
html_fname = 'test_page.html'

@pytest.fixture
def client(request):
    test_client = main.app.test_client()

    def teardown():
        pass # databases and resourses have to be freed at the end. But so far we don't have anything

    request.addfinalizer(teardown)
    return test_client

def test_connect(client):
    _, response = main.connect()
    assert response.status == 200

def test_index(client):
    response = client.get(url + '/')
    assert b'"www.bestfightodds.com API"' == response.data

def test_get_event_list():
	'''
	Dynamic web-page, so test functionality with saved static web-page.
	'''
	html = open(html_fname, 'r', encoding='utf-8').read()
	soup = BeautifulSoup(html, 'html.parser')
	json_response = main.get_event_list(soup)

	assert json_response == json.dumps({"Bellator 233: Salter vs. van Steenis": "November 8th", 
										"Combate 49: San Antonio": "November 8th", 
										"UFC on ESPN+ 21: Zabit vs. Kattar": "November 9th", 
										"UFC on ESPN+ 22: Blachowicz vs. Jacare": "November 16th", 
										"Combate: Hildago": "December 7th", 
										"UFC 245: Usman vs. Covington": "December 14th", 
										"UFC on ESPN+ 23: Ortega vs. The Korean Zombie": "December 21st"})

def test_odds_makers_list():
	'''
	Dynamic web-page, so test functionality with saved static web-page.
	'''
	html = open(html_fname, 'r', encoding='utf-8').read()
	soup = BeautifulSoup(html, 'html.parser')
	json_response = main.odds_makers_list(soup)

	assert json_response == json.dumps(["5Dimes", 
										"Bet365", 
										"BetDSI", 
										"BetOnline", 
										"BookMaker", 
										"Bovada", 
										"Intertops", 
										"Pinnacle", 
										"SportBet", 
										"SportsInt.", 
										"Sportsbook", 
										"TheGreek", 
										"William\u00a0H."])

def test_odds_makers_list_helper():
	html = open(html_fname, 'r', encoding='utf-8').read()
	soup = BeautifulSoup(html, 'html.parser')
	bettor_lst = main.odds_makers_list_helper(soup)

	assert bettor_lst == ["5Dimes", 
						  "Bet365", 
						  "BetDSI", 
						  "BetOnline", 
						  "BookMaker",
						  "Bovada",
						  "Intertops",
						  "Pinnacle",
						  "SportBet",
						  "SportsInt.",
						  "Sportsbook",
						  "TheGreek",
						  "William\u00a0H."]

def test_get_fighter_list():
	'''
	Dynamic web-page, so test functionality with saved static web-page.
	'''
	html = open(html_fname, 'r', encoding='utf-8').read()
	soup = BeautifulSoup(html, 'html.parser')
	json_response = main.get_fighter_list('1', soup)

	assert json_response == json.dumps({"Combate 49: San Antonio": ["Andre Barquero Morera", 
																	"Eduardo Alvarado Osuna", 
																	"Jason Norwood", 
																	"Jose Caceres", 
																	"Cesar Arzamendia", 
																	"Fernando Gonzalez Trevino", 
																	"Justin Governale", 
																	"Peter Caballero", 
																	"Chris Cortez", 
																	"Oscar Suarez", 
																	"Melissa Cervantes", 
																	"Nadine Mandiau", 
																	"Andy Perez", 
																	"Ray Rodriguez", 
																	"Carlos Melara", 
																	"Roy Sarabia"]})

def test_get_fighter_odds():
	'''
	Dynamic web-page, so test functionality with saved static web-page.
	'''
	html = open(html_fname, 'r', encoding='utf-8').read()
	soup = BeautifulSoup(html, 'html.parser')
	json_response = main.get_fighter_odds('colby+covington', soup)

	assert json_response == json.dumps({"odds": {"5Dimes": "+145", 
												 "Bet365": "", 
												 "BetDSI": "+139", 
												 "BetOnline": "+148", 
												 "BookMaker": "+140", 
												 "Bovada": "+140", 
												 "Intertops": "+115", 
												 "Pinnacle": "+130", 
												 "SportBet": "+145", 
												 "SportsInt.": "+130", 
												 "Sportsbook": "+145", 
												 "TheGreek": "+130", 
												 "William\u00a0H.": ""}, 
										"opponent": "Kamaru Usman"})