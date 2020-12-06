from bs4 import BeautifulSoup
import requests
from datetime import datetime


def scrape_nfl():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/football/nfl?marketFilterId=def&preMatchOnly=true&lang=en"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    # we get a list of length 1, need to index into it
    data = {"NFL": get_odds(r[0])}
    return data

def scrape_soccer():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer?marketFilterId=def&preMatchOnly=true&eventsLimit=100&eventsOffset=0&lang=en"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    # soccer has multiple leagues so our api returns a list of objects with events
    data = {"SOC": []}
    print(len(r))
    for games in r:
        game_odds = get_odds(games)
        data["SOC"].extend(game_odds)
    return data

def get_odds(games):
    game_odds = []
    for game in games['events']:
        point_spreads = None
        moneyline = None
        over_under = None
        # gets date of game, need to divide timestamp by factor of 1000
        date = datetime.fromtimestamp(game["startTime"]/1000)
        teams = [team["name"] for team in game["competitors"]]
        point_spreads_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == "Goal Spread"]
        if (point_spreads_dict):
            point_spreads = [
                {
                    "team": team["description"],
                    "handicap": team["price"]["handicap"],
                    "price": team["price"]["american"]
                }
                for team in point_spreads_dict[0]["outcomes"]
            ]
       
        moneyline_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == "3-Way Moneyline"]
        if (moneyline_dict):
            moneyline = [
                {
                    "team": team["description"],
                    "price": team["price"]["american"]
                }
                for team in moneyline_dict[0]["outcomes"]
            ]
        over_under_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == "Total"]
        if (over_under_dict):
            over_under = [
                {
                    "type": team["description"],
                    "handicap": team["price"]["handicap"],
                    "price": team["price"]["american"]
                }
                for team in over_under_dict[0]["outcomes"]
            ]
        line = {
            "date": date, 
            "teams": teams, 
            "point spread": point_spreads,
            "moneyline": moneyline, 
            "O/U": over_under         
        }
        game_odds.append(line)
    return game_odds

print(scrape_soccer())