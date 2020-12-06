import requests

from bs4 import BeautifulSoup


def sports_book_scraper():
    # oddsshark
    # url = 'https://www.oddsshark.com/ncaaf/odds'

    # sportsbook nfl
    url = 'https://www.sportsbook.com/sbk/sportsbook4/nfl-betting/nfl-game-lines.sbk'

    # sportsbook ncaa basketball
    # url = 'https://www.sportsbook.com/sbk/sportsbook4/ncaa-football-betting/game-lines.sbk'

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    event_date = soup.findAll(class_="eventbox")
    odds_list = soup.findAll(class_="market")
    team_name = soup.findAll(class_="team-title")

    i = 0
    a = 0
    g = 0

    # need to add date
    list_of_games = []
    while i < len(team_name):
        team_one = {"index": g, "team": team_name[i].text, "O/U": odds_list[a].text,
                    "spread": odds_list[a + 1].text, "moneyline": odds_list[a + 2].text}
        team_two = {"index": g, "team": team_name[i + 1].text, "O/U": odds_list[a + 3].text,
                    "spread": odds_list[a + 4].text, "moneyline": odds_list[a + 5].text}
        i += 2
        a += 6
        g += 1
        list_of_games.append(team_one)
        list_of_games.append(team_two)
    print(list_of_games)


#sports_book_scraper()

def sports_plays_scraper():
    url = 'https://www.sportsplays.com/pick/eventList/sport_id/1.html'

        # sportsbook ncaa basketball
        # url = 'https://www.sportsbook.com/sbk/sportsbook4/ncaa-football-betting/game-lines.sbk'
    s = requests.session()

    login_data = {
        'username' : 'edward30@my.canisius.edu',
        'password': 'spo12344te',
    }
    response = s.post(url, data=login_data)

#entry point for url

    r = s.get('https://www.sportsplays.com/pick/eventList/sport_id/1.html')
    soup = BeautifulSoup(r.content, 'html.parser')
    bet_table = soup.find(id = 'ajax_tabs_event_list')
    tr_s = bet_table.findAll('tr')
    #starting point of table is 3
    i = 3
    #might be minus 2
    table_end = len(tr_s) - 1
    #total rows
    print(table_end)

    date = None
    game_odds = []
    line = None
    while i < table_end:
        td_s = tr_s[i].findAll('td')
        if len(td_s) < 2:
            game_date = td_s[0].text
        else:
            date = game_date
            teams = td_s[1].text.strip()
            point_spreads = td_s[2].text.strip()
            over_under = td_s[3].text.strip()
            moneyline = td_s[4].text.strip()
            line = {
                "date": date, "teams": teams, "point spread": point_spreads,
                "moneyline": moneyline, "O/U": over_under
            }
            game_odds.append(line)
        i += 1

    print(game_odds[6]['O/U'])
    return game_odds

sports_plays_scraper()
