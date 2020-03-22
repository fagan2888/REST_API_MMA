import urllib
from bs4 import BeautifulSoup
import json
import requests
import regex

def get_html_from_url(url: str = 'https://www.bestfightodds.com/'):
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

def get_num_events(soup=None):
    if not soup:
        soup, error = get_html_from_url()
        if not soup: return error

    events = soup.findAll('div', id=lambda x: x and x.startswith('event'))
    events = [event for event in events if not event.text.startswith('Future Events')]

    return len(events)

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
    
    num_events = get_num_events(soup)

    ## event id validity check ##
    if event_id.isdigit():
        event_id = int(event_id)

        if (event_id > num_events):
            return f'Number of events are: {num_events}. Select an event number between 1 and {num_events}.'
        elif (event_id <= 0):
            return f'Number of events are: {num_events}. Select an event number between 1 and {num_events}.'
    else:
        return 'Not a valid event number.'
    
    tbls_fighters = soup.find_all('div', {'class': 'table-inner-wrapper'})
    tbl = tbls_fighters[event_id-1]

    ## fighter list ##
    fighter_list = []
    for span in tbl.find_all('span', {'class':'tw'}):
        if span.text[0].isalpha() and span.text != 'n/a':
            fighter_list.append(span.text)
    
    ## event title ##
    tbls_events = soup.find_all('div', {'class': 'table-header'})
    tbl = tbls_events[event_id-1]
    event_title = [a_href.text for a_href in tbl.find_all('a', href=True) if a_href['href'].startswith('/events/')][0]

    json_fighter_list = {event_title: fighter_list}
    
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
    re = regex.compile(r'\+\d*')
    
    if fighter.isdigit():
        return 'Invalid fighter name. Separate first and last name by "+".'

    if not soup:
        soup, error = get_html_from_url()
        if not soup: return error

    spans_fighter = [x for x in soup.find_all('span', {'class':'tw'}) if x.text.lower() == fighter.lower()]
    if not spans_fighter:
        return 'Fighter name not found. Separate first and last name by a +.'

    td = spans_fighter[1] ## always take second one ##

    for bettor in odds_makers_list_helper(soup):
        td = td.find_next('td')
        odds_dic[bettor] = re.findall(td.text)[0] if td.text else ''

    fighters_even_lst = [x.find('span', {'class':'tw'}).text.lower() for x in soup.find_all('tr', {'class':'even'})]
    fighters_odd_lst = [x.find('span', {'class':'tw'}).text.lower() for x in soup.find_all('tr', {'class':'odd'})]

    if fighter in fighters_even_lst:
        opponent = fighters_odd_lst[fighters_even_lst.index(fighter)].title()
    else:
        opponent = fighters_even_lst[fighters_odd_lst.index(fighter)].title()

    fighter_odds_dic = {'odds': odds_dic,
                        'opponent': opponent}

    json_fighter_odds = fighter_odds_dic

    return json_fighter_odds
