import requests

from bs4 import BeautifulSoup

def url_scraper():
    url = 'https://www.sportsplays.com/make-pick.html'

    # sportsbook ncaa basketball
    # url = 'https://www.sportsbook.com/sbk/sportsbook4/ncaa-football-betting/game-lines.sbk'
    s = requests.session()

    login_data = {
        'username' : 'edward30@my.canisius.edu',
        'password': 'spo12344te',
    }
    response = s.post(url, data=login_data)
    r = s.get('https://www.sportsplays.com/make-pick.html')
    soup = BeautifulSoup(r.content, 'html.parser')
    #locates tab with urls and pulls them
    sports_tabs = soup.find(id = 'sports_tabs')
    anchor_tags = sports_tabs.findAll('a')
    num_anchors = len(anchor_tags)

    url_first_piece = 'https://www.sportsplays.com'
    url_last_peice_game = '.html'
    url_last_peice_first_half = '/pick_type/first_half.html'
    url_last_peice_first_quarter = '/pick_type/first_quarter.html'
    url_last_peice_second_half = '/pick_type/second_half.html'
    #starts at second index
    x = 2
    url_list_of_sec = []
    final_link_list = []
    i=0
    #creates a list of the second piece of urls
    while x < num_anchors:
        url_second_piece = anchor_tags[x].get('href')
        url_list_of_sec.append(url_second_piece[:-5])
        x+=1

    while i < len(url_list_of_sec):
        final_link = url_first_piece + url_list_of_sec[i] + url_last_peice_game
        final_link_list.append(final_link)
        final_link = url_first_piece + url_list_of_sec[i] + url_last_peice_first_half
        final_link_list.append(final_link)
        final_link = url_first_piece + url_list_of_sec[i] + url_last_peice_first_quarter
        final_link_list.append(final_link)
        final_link = url_first_piece + url_list_of_sec[i] + url_last_peice_second_half
        final_link_list.append(final_link)
        i += 1
    print('final link list:')
    print(final_link_list)
    return (final_link_list)

# def sp_URLs


def sports_plays_scraper(scraped_url):
    url = 'https://www.sportsplays.com/my-page.html'

    s = requests.session()

    login_data = {
        'username' : '',
        'password': '',
    }

    response = s.post(url, data=login_data)
    print('url length:')
    print(len(scraped_url))

    for link in scraped_url:
        url = link
#entry point for url
        print(url)
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bet_table = soup.find(id = 'ajax_tabs_event_list')
        tr_s = bet_table.findAll('tr')
        #starting point of table is 3
        i = 3
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
            td_s = tr_s[i].findAll('td')
            if len(td_s) < 2:
                #print(td_s[0])
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

        print(game_odds)
        #return game_odds

sports_plays_scraper(url_scraper())

#print(len(tr))
#print(tr[57].text)
#print(td[1].text)
#url_scraper()
