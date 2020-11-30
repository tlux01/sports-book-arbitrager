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

#url of nfl picks
url = 'https://www.sportsplays.com/pick/eventList/sport_id/1.html'

    # sportsbook ncaa basketball
    # url = 'https://www.sportsbook.com/sbk/sportsbook4/ncaa-football-betting/game-lines.sbk'
s = requests.session()

login_data = {
    'username' : 'edward30@my.canisius.edu',
    'password': 'spo12344te',
}
response = s.post(url, data=login_data)
r = s.get('https://www.sportsplays.com/pick/eventList/sport_id/1.html')
soup = BeautifulSoup(r.content, 'html.parser')
bet_table = soup.find(id = 'ajax_tabs_event_list')
tr = bet_table.findAll('tr')
td = tr[3].findAll('td')
#rows = bet_table.findAll('tr')

#cut out extra will want to make dynamic eventually
#date row starts at tr[3] and ends len(tr)-2
i = 3
table_end = len(tr) - 1
print(table_end)

#break up only tr you need: i is start and table_end is the end
while i < table_end:
    print(i)
    i += 1

#print(len(tr))
#print(tr[57].text)
#print(td[0].text)
sports_book_scraper()