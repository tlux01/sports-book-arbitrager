import requests

from bs4 import BeautifulSoup

with open('auth.txt', 'r') as f:
    credentials = f.readlines()
    user_name = credentials[0].strip('\n')
    password = credentials[1].strip('\n')

#normal urls
nfl_url = ['https://www.sportsplays.com/pick/eventList/sport_id/1.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_half.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_quarter.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/second_half.html']

college_football = ['https://www.sportsplays.com/pick/eventList/sport_id/2.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/first_half.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/first_quarter.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/second_half.html']

nba_basketball= ['https://www.sportsplays.com/pick/eventList/sport_id/4.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/first_half.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/first_quarter.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/second_half.html']

college_basketball = ['https://www.sportsplays.com/pick/eventList/sport_id/5.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/first_half.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/first_quarter.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/second_half.html']

golf = ['https://www.sportsplays.com/pick/eventList/sport_id/19.html']

tennis = [ 'https://www.sportsplays.com/pick/eventList/sport_id/12.html']

#abnormal urls
soccer = ['https://www.sportsplays.com/pick/eventList/sport_id/10.html']

fighting = ['https://www.sportsplays.com/pick/eventList/sport_id/13.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/first_half.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/first_quarter.html',
 'https://www.sportsplays.com/pick/eventList/sport_id/13/pick_type/second_half.html']





# def sp_URLs

def nfl_sp_scraper():
    nfl_url = ['https://www.sportsplays.com/pick/eventList/sport_id/1.html',
               'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_half.html',
               'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/first_quarter.html',
               'https://www.sportsplays.com/pick/eventList/sport_id/1/pick_type/second_half.html']
    url = 'https://www.sportsplays.com/my-page.html'
    s = requests.session()
    login_data = {
        'username' : user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(nfl_url))

    for link in nfl_url:
        url = link
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
        game_odds = []

        ##### soccer gets messed up because their is some extra stuff at top
        # can find stat of table by name = 'TIMEZONE'

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if len(td_s) < 2:
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                line = {
                    "type":"nfl", "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def college_football_sp_scraper():
    college_football = ['https://www.sportsplays.com/pick/eventList/sport_id/2.html',
                        'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/first_half.html',
                        'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/first_quarter.html',
                        'https://www.sportsplays.com/pick/eventList/sport_id/2/pick_type/second_half.html']
    url = 'https://www.sportsplays.com/my-page.html'
    s = requests.session()

    login_data = {
        'username' : user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(college_football))

    for link in college_football:
        url = link
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
        game_odds = []

        ##### soccer gets messed up because their is some extra stuff at top
        # can find stat of table by name = 'TIMEZONE'

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if len(td_s) < 2:
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                line = {
                    "type":"cfb", "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def nba_sp_scraper():
    nba_basketball = ['https://www.sportsplays.com/pick/eventList/sport_id/4.html',
                      'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/first_half.html',
                      'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/first_quarter.html',
                      'https://www.sportsplays.com/pick/eventList/sport_id/4/pick_type/second_half.html']
    url = 'https://www.sportsplays.com/my-page.html'

    s = requests.session()

    login_data = {
        'username' : user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(nba_basketball))

    for link in nba_basketball:
        url = link
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
        game_odds = []

        ##### soccer gets messed up because their is some extra stuff at top
        # can find stat of table by name = 'TIMEZONE'

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if len(td_s) < 2:
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                line = {
                    "type":"nba", "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def college_basketball_sp_scraper():
    college_basketball = ['https://www.sportsplays.com/pick/eventList/sport_id/5.html',
                          'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/first_half.html',
                          'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/first_quarter.html',
                          'https://www.sportsplays.com/pick/eventList/sport_id/5/pick_type/second_half.html']
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
        url = link
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
        game_odds = []

        ##### soccer gets messed up because their is some extra stuff at top
        # can find stat of table by name = 'TIMEZONE'

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if len(td_s) < 2:
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                line = {
                    "type": "cbb", "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def golf_sp_scraper():
    golf = ['https://www.sportsplays.com/pick/eventList/sport_id/19.html']
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
        url = link
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
        game_odds = []

        ##### soccer gets messed up because their is some extra stuff at top
        # can find stat of table by name = 'TIMEZONE'

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if len(td_s) < 2:
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                line = {
                    "type" : "golf", "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)

def tennis_sp_scraper():
    tennis = ['https://www.sportsplays.com/pick/eventList/sport_id/12.html']
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
        url = link
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
        game_odds = []

        ##### soccer gets messed up because their is some extra stuff at top
        # can find stat of table by name = 'TIMEZONE'

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')
            #finds if row is a date and then sets it as a date
            #might want to find a better way to identify that
            if len(td_s) < 2:
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                over_under = td_s[3].text.strip()
                moneyline = td_s[4].text.strip()
                line = {
                    "type" : "tennis", "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)


def soccer_sp_scraper():
    soccer = ['https://www.sportsplays.com/pick/eventList/sport_id/10.html']
    url = 'https://www.sportsplays.com/my-page.html'

    s = requests.session()

    login_data = {
        'username' : user_name,
        'password': password,
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(soccer))

    for link in soccer:
        url = link
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
        game_odds = []

        ##### soccer gets messed up because their is some extra stuff at top
        # can find stat of table by name = 'TIMEZONE'

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')

            #finds if row is a date and then sets it as a date
            if len(td_s) < 2:
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
                line = {
                    "type" : "soccer", "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline, "O/U": over_under
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)
        #return game_odds


def fighting_sp_scraper():
    fighting = ['https://www.sportsplays.com/pick/eventList/sport_id/13.html']
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
        url = link
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
        game_odds = []
        line = None

        ##### soccer gets messed up because their is some extra stuff at top
        # can find stat of table by name = 'TIMEZONE'

        while i < table_end:
            #finds cells in row
            td_s = tr_s[i].findAll('td')

            #finds if row is a date and then sets it as a date
            if len(td_s) < 2:
                #print(td_s[0])
                game_date = td_s[0].text
            else:
                #else determines it is a game row
                date = game_date
                teams = td_s[1].text.strip()
                point_spreads = td_s[2].text.strip()
                moneyline = td_s[3].text.strip()
                line = {
                    "type": 'fighting', "date": date, "teams": teams, "point spread": point_spreads,
                    "moneyline": moneyline
                }
                #captures odds
                game_odds.append(line)
            i += 1

        print(game_odds)



nfl_sp_scraper()
