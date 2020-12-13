import requests
from bs4 import BeautifulSoup
import pprint
from datetime import datetime
import re

# sportsplays cookie is responsible for keeping you logged in v
def create_sportsplays_session():
    # reading from auth.txt file credentials for sportsplays
    with open('auth.txt', 'r') as f:
        credentials = f.readlines()
        user_name = credentials[0].strip('\n')
        password = credentials[1].strip('\n')
    
    login_url = 'https://www.sportsplays.com/login.html'
    session = requests.session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

    login_data = {
        'username' : user_name,
        'password': password,
    }

    session.post(login_url, data=login_data)
    return session

session = create_sportsplays_session()

def find_start(tr_list):
    for i,tr in enumerate(tr_list):
        if tr.find('th'):
            return i

def find_end(tr_list):
    for i,tr in enumerate(tr_list):
        table_data = tr.findAll('td')
        if len(table_data) == 1 and table_data[0].get_text(strip=True) == '':
            return i

def parse_moneyline(moneyline_txt, team):
    moneyline = {
        "team": team,
        "price": moneyline_txt
    } if moneyline_txt != "" else None
    return moneyline

def parse_spread(point_spread_txt, team):
    point_spread = {
        "team": team,
        "price": re.search('[(]?[+,-]\d*[)]', point_spread_txt).group().strip('(').strip(')'),
        "handicap": re.search('[+,-]?\d*[.]?\d*', point_spread_txt).group()
    } if point_spread_txt != "" else None
    return point_spread  

def parse_over_under(over_under_txt):
    over_under = None
    if over_under_txt == "":
        return None
    else:
        if over_under_txt[0] == "O":
            over_under = {
                "type": 'Over',
                "price": re.search('[(]?[+,-]\d*[)]', over_under_txt).group().strip('(').strip(')'),
                "handicap": re.search('[+,-]?\d*[.]?\d*', over_under_txt).group()
            }
        elif over_under_txt[0] == "U":
            over_under = {
                "type": 'Under',
                "price": re.search('[(]?[+,-]\d*[)]', over_under_txt).group().strip('(').strip(')'),
                "handicap": re.search('[+,-]?\d*[.]?\d*', over_under_txt).group()
            }
    return over_under

def nfl_sp_scraper(session):
    #session = create_sportsplays_session()
    nfl_url = {'Total Game': 'https://www.sportsplays.com/pick/eventList/sport_id/1.html',
               'First Half': 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_half.html',
               'First Quarter': 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_quarter.html',
               'Second Quarter': 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/second_half.html'}
    data = {}
    for period in nfl_url:
        url = nfl_url[period]
        game_odds = []
        #entry point for url
        r = session.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_list = bet_table.findAll('tr')
        # skip over if tr_list is empty
        if len(tr_list) == 0:
            data[period] = game_odds
            continue
        start = find_start(tr_list)
        end = find_end(tr_list)
        # block size of 2 a only 2 rows per game
        game_block_size = 2
        game_date = None
        
        i = start + 1
        while i < end:
            tr = tr_list[i]
            td_list = tr.findAll('td')
            if td_list[0].find('strong'):
                i += 1
                game_date = td_list[0].text.strip('\n').strip('(All Times EST)')
                
            else:
                i += game_block_size
                point_spreads = []
                moneylines = []
                over_under = []
                teams = []
                game_time = None
                for row in range(game_block_size):
                    if td_list[0].text.strip() != '':
                        game_time = game_date + ' ' + td_list[0].text.strip()
                        game_time = datetime.strptime(game_time, '%B %d, %Y %I:%M%p')

                    team = td_list[1].text.strip()
                    point_spread_txt = td_list[2].text.strip()
                    over_under_txt = td_list[3].text.strip()
                    moneyline_txt = td_list[4].text.strip()
                    
                    teams.append(team)
                    moneylines.append(parse_moneyline(moneyline_txt, team))
                    point_spreads.append(parse_spread(point_spread_txt, team))
                    over_under.append(parse_over_under(over_under_txt))
                line = {
                    "date": game_time, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneylines, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
        data[period] = game_odds
    return data
                        

pprint.pprint(nfl_sp_scraper(session))
