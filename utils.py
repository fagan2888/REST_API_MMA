import urllib
from bs4 import BeautifulSoup
import json
import requests

def get_html_from_url(url: str = 'https://www.bestfightodds.com/') -> str:
    '''
    Gets HTML from url w/ error handling.
    
    Input
    -------
    url
    
    Returns
    --------
    HTML text or None (if error)
    r.status_code or http error msg
    '''
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent}

    try:
        r = requests.get(url, headers=headers, timeout=3)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup, r.status_code
        else:
            return None, f'Invalid HTML status code {r.status_code}'
    except requests.exceptions.HTTPError as e:
        return None, f'Http Error: {e}'
    except requests.exceptions.ConnectionError as e:
        return None, f'Error Connecting: {e}'
    except requests.exceptions.Timeout as e:
        return None, f'Timeout Error: {e}'
    except requests.exceptions.RequestException as e:
        return None, f'Url error: {e}'

def connect():
    '''
    Pulls page from url and converts to beautifulsoup object, to then be used by other funcs.
    '''

    html = get_html_from_url()
    soup = BeautifulSoup(html, 'html.parser')

    return soup, response
        
def get_event_list(soup=None):
    '''
    Parses list of events and their dates. Returns json object.
    '''
    if not soup:
        soup, error = get_html_from_url()
        if not soup: return error
    
    event_list = [a_href.text for a_href in soup.find_all('a', href=True) if a_href['href'].startswith('/events')]
    event_dates = [span.text for span in soup.find_all('span', {'class': 'table-header-date'})]
    json_events = {k:v for k,v in zip(event_list, event_dates)}

    return json_events

def get_odds_makers_list(soup=None):
    '''
    Parses list of bettors. Returns json object.
    '''
    if not soup:
        soup, error = get_html_from_url()
        if not soup: return error
    
    odds_maker_list = sorted(list(set([a_href.text for a_href in soup.find_all('a', href=True) if a_href['href'].startswith('/out/')])))
    json_odds_makers = odds_maker_list
    
    return json_odds_makers

def odds_makers_list_helper(soup):
    odds_maker_list = sorted(list(set([a_href.text for a_href in soup.find_all('a', href=True) if a_href['href'].startswith('/out/')])))
    return odds_maker_list

def get_fighter_list(event_id, soup=None):
    '''
    Parses list of fighters for a particular event id. Event id is an int ordering by date occuring.
    Returns the event name and list of fighters as json object.
    If the event id is not an int, less than 0, or greater than the # of events, it's invalid.
    '''
    if not soup:
        soup, error = get_html_from_url()
        if not soup: return error
    
    tbls_fighters = soup.find_all('div', {'class': 'table-inner-wrapper'})

    ## event id validity check ##
    if event_id.isdigit():
        event_id = int(event_id)
        if (event_id >= 0) and (event_id < len(tbls_fighters)):
            tbl = tbls_fighters[event_id]
        else:
            return 'Invalid event number'
    else:
        return 'Invalid event number'
    
    ## fighter list ##
    fighter_list = []
    for span in tbl.find_all('span', {'class':'tw'}):
        if span.text[0].isalpha() and span.text != 'n/a':
            fighter_list.append(span.text)
    
    ## event title ##
    tbls_events = soup.find_all('div', {'class': 'table-header'})
    tbl = tbls_events[event_id]
    event_title = [a_href.text for a_href in tbl.find_all('a', href=True) if a_href['href'].startswith('/events/')][0]

    json_fighter_list = json.dumps({event_title: fighter_list})
    
    return json_fighter_list

def get_fighter_odds(fighter_name, soup=None):
    '''
    Pulls odds for inputted fighter for first event they're present on sorted by date.
    Also returns opponent's name. Can search for opponent's odds with same API call with oponent name.
    Combine name with spaces (i.e. jon jones as jon+jones).
    '''
    odds_dic = {}
    opponent = ''
    fighter = ' '.join(fighter_name.split('+')).lower()
    
    if fighter.isdigit():
        return 'Invalid fighter name. Separate first and last name by "+".'

    if not soup:
        soup, error = connect()
        if not soup: return error

    spans_fighter = [x for x in soup.find_all('span', {'class':'tw'}) if x.text.lower() == fighter.lower()]
    if not spans_fighter:
        return 'Fighter name not found. Separate first and last name by "+".'

    td = spans_fighter[1] ## always take second one ##

    for bettor in odds_makers_list_helper(soup):
        td = td.find_next('td')
        odds_dic[bettor] = td.text.replace('▲', '').replace('▼', '')

    opponent = td.find_next('span', {'class':'tw'}).find_next('span', {'class':'tw'}).text

    fighter_odds_dic = {'odds': odds_dic,
                        'opponent': opponent}

    json_fighter_odds = json.dumps(fighter_odds_dic)

    return json_fighter_odds
