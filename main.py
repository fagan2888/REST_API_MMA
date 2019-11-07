from flask import Flask, request
import urllib
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'www.bestfightodds.com API'
        
def connect():
    '''
    Pulls page from url and converts to beautifulsoup object, to then be used by other funcs.
    '''
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 

    url = 'https://www.bestfightodds.com/'
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    return soup
        
@app.route('/event_list')
def get_event_list():
    '''
    Parses list of events and their dates. Returns json object.
    '''
    soup = connect()
    
    event_list = [a_href.text for a_href in soup.find_all('a', href=True) if a_href['href'].startswith('/events')]
    event_dates = [span.text for span in soup.find_all('span', {'class': 'table-header-date'})]
    json_events = json.dumps({k:v for k,v in zip(event_list, event_dates)})

    return json_events

@app.route('/odds_makers_list')
def get_bettor_list():
    '''
    Parses list of bettors. Returns json object.
    '''
    soup = connect()
    
    odds_maker_list = sorted(list(set([a_href.text for a_href in soup.find_all('a', href=True) if a_href['href'].startswith('/out/')])))
    json_odds_makers = json.dumps(odds_maker_list)
    
    return json_odds_makers

def get_bettor_list_helper(soup):
    odds_maker_list = sorted(list(set([a_href.text for a_href in soup.find_all('a', href=True) if a_href['href'].startswith('/out/')])))
    return odds_maker_list

@app.route('/fighter_list/<id_>')
def get_fighter_list(id_):
    '''
    Parses list of fighters for a particular event id. Event id is an int ordering by date occuring.
    Returns the event name and list of fighters as json object.
    If the event id is not an int, less than 0, or greater than the # of events, it's invalid.
    '''
    soup = connect()
    
    tbls_fighters = soup.find_all('div', {'class': 'table-inner-wrapper'})

    ## event id validity check ##
    if id_.isdigit():
        id_ = int(id_)
        if (id_ >= 0) and (id_ < len(tbls_fighters)):
            tbl = tbls_fighters[id_]
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
    tbl = tbls_events[id_]
    event_title = [a_href.text for a_href in tbl.find_all('a', href=True) if a_href['href'].startswith('/events/')][0]

    json_fighter_list = json.dumps({event_title: fighter_list})
    
    return json_fighter_list

@app.route('/odds/<fighter_name>')
def get_fighter_odds(fighter_name):
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

    soup = connect()

    spans_fighter = [x for x in soup.find_all('span', {'class':'tw'}) if x.text.lower() == fighter.lower()]
    if not spans_fighter:
        return 'Fighter name not found. Separate first and last name by "+".'

    td = spans_fighter[1] ## always take second one ##

    for bettor in get_bettor_list_helper(soup):
        td = td.find_next('td')
        odds_dic[bettor] = td.text.replace('▲', '').replace('▼', '')

    opponent = td.find_next('span', {'class':'tw'}).find_next('span', {'class':'tw'}).text

    fighter_odds_dic = {'odds': odds_dic,
                        'opponent': opponent}

    json_fighter_odds = json.dumps(fighter_odds_dic)

    return json_fighter_odds

if __name__ == '__main__':
	app.run(host='0.0.0.0')