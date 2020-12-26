from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pprint

KEYWORDS = {
    'DEFAULT': {
        "Spread" : "Point Spread",
        "Moneyline" : "Moneyline",
        "O/U" : "Total"
    },
    'SOC': {
        "Spread" : "Goal Spread",
        "Moneyline" : "3-Way Moneyline",
        "O/U" : "Total"
    }    
}


def nfl_bv_scraper():
    urls = {
        "Total Game": "https://www.bovada.lv/services/sports/event/coupon/events/A/description/football/nfl?marketFilterId=def&preMatchOnly=true&lang=en",
        "First Half": "https://www.bovada.lv/services/sports/event/coupon/events/A/description/football/nfl?marketFilterId=701&preMatchOnly=true&lang=en"
    }
    data = {}
    # we get a list of length 1, need to index into it
    for period in urls:
        r = requests.get(urls[period], headers={'User-Agent': 'Mozilla/5.0'}).json()
        # NFL is its own league, so list is of size one
        odds = get_odds(r[0], "DEFAULT")
        data[period] = odds
    return data

def soccer_bv_scraper():
    urls = {"Total Game": "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer?marketFilterId=def&preMatchOnly=true&eventsLimit=1000&eventsOffset=0&lang=en"}
    # soccer has multiple leagues so our api returns a list of objects with events
    data = {}
    for period in urls:
        url = urls[period]
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
        odds_list = []
        for games in r:
            odds = get_odds(games, "SOC")
            odds_list.extend(odds)
        data[period] = odds_list
    return data

def nba_bv_scraper():
    urls = {
        "Total Game" : "https://www.bovada.lv/services/sports/event/coupon/events/A/description/basketball/nba?marketFilterId=def&preMatchOnly=true&lang=en"
    }
    data = {}
    for period in urls:
        r = requests.get(urls[period], headers={'User-Agent': 'Mozilla/5.0'}).json()
        # NFL is its own league, so list is of size one
        odds = get_odds(r[0], "DEFAULT")
        data[period] = odds
    return data

def get_odds(games, sport):
    game_odds = []
    for game in games['events']:
        point_spreads = None
        moneylines = None
        over_unders = None
        # gets date of game, need to divide timestamp by factor of 1000
        date = datetime.fromtimestamp(game["startTime"]/1000)
        teams = [team["name"] for team in game["competitors"]]
        point_spreads_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == KEYWORDS[sport]["Spread"]]
        if (point_spreads_dict and point_spreads_dict[0]["outcomes"]):
            point_spreads = {}
            for team in point_spreads_dict[0]["outcomes"]:
                point_spread = {
                    team["description"]: {
                        "handicap": team["price"]["handicap"],
                        "price": team["price"]["american"]
                    }
                }
                point_spreads = {**point_spreads, **point_spread}
       
        moneyline_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == KEYWORDS[sport]["Moneyline"]]
        if (moneyline_dict and moneyline_dict[0]["outcomes"]):
            moneylines = {}
            for team in moneyline_dict[0]["outcomes"]:
                moneyline = {
                    team["description"] : {
                        "price": team["price"]["american"]
                    }
                }
                moneylines = {**moneylines, **moneyline}

        over_under_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == KEYWORDS[sport]["O/U"]]
        if (over_under_dict and over_under_dict[0]["outcomes"]):
            over_unders = {}
            for team in over_under_dict[0]["outcomes"]:
                over_under = {
                    team["description"]: {
                        "handicap": team["price"]["handicap"],
                        "price": team["price"]["american"]
                    }
                }
            over_unders = {**over_unders, **over_under}
                    
        line = {
            "date": date, 
            "teams": teams, 
            "point spread": point_spreads,
            "moneyline": moneylines, 
            "O/U": over_unders         
        }
        game_odds.append(line)
    return game_odds
