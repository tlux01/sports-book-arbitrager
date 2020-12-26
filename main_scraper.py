import requests

from bs4 import BeautifulSoup
import pprint
with open('auth.txt', 'r') as f:
    credentials = f.readlines()
    user_name = credentials[0].strip('\n')
    password = credentials[1].strip('\n')

#normal urls
nfl_url = {'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/1.html',
 'First Half':'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_half.html',
 'First Quarter':'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_quarter.html',
 'Second Quarter':'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/second_half.html'}

college_football = {'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/2.html',
 'First Half':'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/first_half.html',
 'First Quarter':'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/first_quarter.html',
 'Second Half':'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/second_half.html'}

nba_basketball= {'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/4.html',
 'First Half':'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/first_half.html',
 'First Quarter':'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/first_quarter.html',
 'Second Half':'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/second_half.html'}

college_basketball = {'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/5.html',
 'First Half':'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/first_half.html',
 'First Quarter':'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/first_quarter.html',
 'Second Half':'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/second_half.html'}

golf ={'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/19.html'}

tennis = {'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/12.html'}

#abnormal urls
soccer = {'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/10.html'}

fighting = {'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/13.html',
 'First Half':'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/first_half.html',
 'First Quarter':'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/first_quarter.html',
 'Second Half':'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/second_half.html'}

def starter():
    url = 'https://www.sportsplays.com/my-page.html'
    s = requests.session()
    login_data = {
        'username': user_name,
        'password': password,
    }
    response = s.post(url, data=login_data)
    print('function was run')
    return response

# def sp_URLs

def nfl_sp_scraper():
    nfl_url = {'Total Game': 'https://www.sportsplays.com/pick/eventList/sport_id/1.html',
               'First Half': 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_half.html',
               'First Quarter': 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_quarter.html',
               'Second Quarter': 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/second_half.html'}
    url = 'https://www.sportsplays.com/my-page.html'
    s = requests.session()
    login_data = {
        'username': user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(nfl_url))
    data = {}
    for period in nfl_url:
        url = nfl_url[period]
        #entry point for url
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #starting point of table is 3
        #finding true i
        i = 0
        for th in tr_s:
            if th.find('th'):
                i += 1
                #4 for soccer

                break
            i += 1

        #finds the end of the table
        table_end = len(tr_s) - 1

        date = None
        teams = None
        point_spreads = None
        over_under = None
        moneyline = None
        date = None
        time = None
        game_odds = []


        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            if td_s[0].find('strong'):
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date.strip('\n').strip('(All Times EST)')
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                if td_s[0].text.strip() != '':
                    date += " " + td_s[0].text.strip()

                line = {
                    "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
            i += 1
        data[period] = game_odds
    return data

def college_football_sp_scraper():
    college_football = {'Total Game': 'https://www.sportsplays.com/pick/eventList/sport_id/2.html',
                        'First Half': 'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/first_half.html',
                        'First Quarter': 'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/first_quarter.html',
                        'Second Half': 'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/second_half.html'}
    url = 'https://www.sportsplays.com/my-page.html'
    s = requests.session()

    login_data = {
        'username': user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(college_football))

    for link in college_football:
        url = college_football[link]
        period = link
        #entry point for url
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #starting point of table is 3
        #finding true i
        i = 0
        for th in tr_s:
            if th.find('th'):
                i += 1
                #4 for soccer

                break
            i += 1

        #finds the end of the table
        table_end = len(tr_s) - 1

        date = None
        teams = None
        point_spreads = None
        over_under = None
        moneyline = None
        date = None
        time = None
        game_odds = []

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if td_s[0].find('strong'):
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                if td_s[0].text.strip() != '':
                    time = td_s[0].text.strip()

                line = {
                    "type": "cfb", "date": date, "time": time, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under, "period": period
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def nba_sp_scraper():
    nba_basketball = {'Total Game': 'https://www.sportsplays.com/pick/eventList/sport_id/4.html',
                      'First Half': 'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/first_half.html',
                      'First Quarter': 'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/first_quarter.html',
                      'Second Half': 'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/second_half.html'}
    url = 'https://www.sportsplays.com/my-page.html'

    s = requests.session()

    login_data = {
        'username': user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(nba_basketball))

    for link in nba_basketball:
        url = nba_basketball[link]
        period = link
        #entry point for url
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #starting point of table is 3
        #finding true i
        i=0
        for th in tr_s:
            if th.find('th'):
                i += 1
                #4 for soccer

                break
            i += 1

        #finds the end of the table
        table_end = len(tr_s) - 1

        date = None
        teams = None
        point_spreads = None
        over_under = None
        moneyline = None
        date = None
        time = None
        game_odds = []


        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if td_s[0].find('strong'):
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                if td_s[0].text.strip()!='':
                    time = td_s[0].text.strip()

                line = {
                    "type": "nba", "date": date, "time": time, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under, "period": period
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def college_basketball_sp_scraper():
    college_basketball = {'Total Game': 'https://www.sportsplays.com/pick/eventList/sport_id/5.html',
                          'First Half': 'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/first_half.html',
                          'First Quarter': 'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/first_quarter.html',
                          'Second Half': 'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/second_half.html'}
    url = 'https://www.sportsplays.com/my-page.html'

    s = requests.session()

    login_data = {
        'username' : user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(college_basketball))

    for link in college_basketball:
        url = college_basketball[link]
        period = link
        #entry point for url
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #starting point of table is 3
        #finding true i
        i=0
        for th in tr_s:
            if th.find('th'):
                i += 1
                #4 for soccer

                break
            i += 1

        #finds the end of the table
        table_end = len(tr_s) - 1

        date = None
        teams = None
        point_spreads = None
        over_under = None
        moneyline = None
        date = None
        time = None
        game_odds = []


        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if td_s[0].find('strong'):
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                if td_s[0].text.strip()!='':
                    time = td_s[0].text.strip()

                line = {
                    "type": "cbb", "date": date, "time": time, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under, "period": period
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def golf_sp_scraper():
    golf ={'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/19.html'}
    url = 'https://www.sportsplays.com/my-page.html'
    s = requests.session()

    login_data = {
        'username' : user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(golf))

    for link in golf:
        url = golf[link]
        period = link
        #entry point for url
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #starting point of table is 3
        #finding true i
        i=0
        for th in tr_s:
            if th.find('th'):
                i += 1
                #4 for soccer

                break
            i += 1

        #finds the end of the table
        table_end = len(tr_s) - 1

        date = None
        teams = None
        point_spreads = None
        over_under = None
        moneyline = None
        date = None
        time = None
        game_odds = []


        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if td_s[0].find('strong'):
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                if td_s[0].text.strip()!='':
                    time = td_s[0].text.strip()

                line = {
                    "type" : "golf", "date": date, "time":time, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under, "period": period
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def tennis_sp_scraper():
    tennis = {'Total Game': 'https://www.sportsplays.com/pick/eventList/sport_id/12.html'}
    url = 'https://www.sportsplays.com/my-page.html'

    s = requests.session()

    login_data = {
        'username' : user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(tennis))

    for link in tennis:
        url = tennis[link]
        period = link
        #entry point for url
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #starting point of table is 3
        #finding true i
        i=0
        for th in tr_s:
            if th.find('th'):
                i += 1
                #4 for soccer

                break
            i += 1

        #finds the end of the table
        table_end = len(tr_s) - 1

        date = None
        teams = None
        point_spreads = None
        over_under = None
        moneyline = None
        date = None
        time = None
        game_odds = []



        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if td_s[0].find('strong'):
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                if td_s[0].text.strip()!='':
                    time = td_s[0].text.strip()

                line = {
                    "type": "tennis", "date": date, "time": time, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under, "period": period
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)


def soccer_sp_scraper():
    soccer = {'Total Game':'https://www.sportsplays.com/pick/eventList/sport_id/10.html'}
    url = 'https://www.sportsplays.com/my-page.html'

    s = requests.session()

    login_data = {
        'username': user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(soccer))

    for link in soccer:
        url = soccer[link]
        period = link
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #finding true stat point
        i=0
        for th in tr_s:
            if th.find('th'):
                i += 1
                #4 for soccer

                break
            i += 1
        #finds table end
        table_end = len(tr_s) - 1
        date = None
        teams = None
        point_spreads = None
        over_under = None
        moneyline = None
        date = None
        time = None
        game_odds = []



        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')

            #finds if row is a date and then sets it as a date
            if td_s[0].find('strong'):
                #print(td_s[0])
                game_date = td_s[0].text

            #identifies if it is a Draw row for soccer if there arre exactly 3 cells(td)
            elif len(td_s) == 3:
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = None
                moneyline = None
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                if td_s[0].text.strip()!='':
                    time = td_s[0].text.strip()

                line = {
                    "type": "soccer", "date": date, "time": time, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under, "period": period
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)
        #return game_odds


def fighting_sp_scraper():
    fighting = {'Total Game': 'https://www.sportsplays.com/pick/eventList/sport_id/13.html',
                'First Half': 'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/first_half.html',
                'First Quarter': 'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/first_quarter.html',
                'Second Half': 'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/second_half.html'}
    url = 'https://www.sportsplays.com/my-page.html'

    s = requests.session()

    login_data = {
        'username' : user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(fighting))

    for link in fighting:
        url = fighting[link]
        period = link
        #entry point for url
        print(url)
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #starting point of table is 3
        #finding true i
        i=0
        for th in tr_s:
            if th.find('th'):
                i += 1
                print('true')
                print(i)
                #4 for soccer

                break
            i += 1

            #print(table_begin[0].text)
            #print('test:')
            #print(table_begin)

        #i = 3
        #might be minus 2
        table_end = len(tr_s) - 1
        #total rows
        print('number of rows on page:')
        print(table_end)

        date = None
        time = None
        game_odds = []
        line = None


        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')

            #finds if row is a date and then sets it as a date
            if td_s[0].find('strong'):
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                moneyline = td_s[3].text.strip()
                if td_s[0].text.strip()!='':
                    time = td_s[0].text.strip()

                line = {
                    "type": 'fighting', "date": date, "time": time, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "period": period
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

#golf_sp_scraper()
#fighting_sp_scraper()
#soccer_sp_scraper()
#college_football_sp_scraper()
pprint.pprint(nfl_sp_scraper())
#tennis_sp_scraper()
#nba_sp_scraper()
#college_basketball_sp_scraper()
