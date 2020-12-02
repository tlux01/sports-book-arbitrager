from bs4 import BeautifulSoup
import requests
from datetime import datetime


def scrape_nfl():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/football/nfl?marketFilterId=def&preMatchOnly=true&lang=en"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    # we get a list of length 1, need to index into it
    games = r[0]["events"]
    game_odds = []
    for game in games:
        print(game)
        # gets date of game, need to divide timestamp by factor of 1000
        date = datetime.fromtimestamp(game["startTime"]/1000)
        teams = [team["name"] for team in game["competitors"]]
        point_spreads_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == "Point Spread"][0]
        point_spreads = [
            {
                "team": team["description"],
                "handicap": team["price"]["handicap"],
                "price": team["price"]["american"]
            }
            for team in point_spreads_dict["outcomes"]
        ]
        moneyline_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == "Moneyline"][0]
        moneyline = [
            {
                "team": team["description"],
                "price": team["price"]["american"]
            }
            for team in moneyline_dict["outcomes"]
        ]
        over_under_dict = [team for team in game["displayGroups"][0]["markets"] 
                                if team["description"] == "Total"][0]
        over_under = [
            {
                "type": team["description"],
                "handicap": team["price"]["handicap"],
                "price": team["price"]["american"]
            }
            for team in over_under_dict["outcomes"]
        ]
        line = {
            "date": date, 
            "teams": teams, 
            "point spread": point_spreads,
            "moneyline": moneyline, 
            "O/U": over_under         
        }
        game_odds.append(line)
    #print(game_odds)
    return game_odds

scrape_nfl()

"""
EXAMPLE output of an game from api
{
   "id":"7995252",
   "description":"Baltimore Ravens @ Pittsburgh Steelers",
   "type":"GAMEEVENT",
   "link":"/football/nfl/baltimore-ravens-pittsburgh-steelers-202012021540",
   "status":"U",
   "sport":"FOOT",
   "startTime":1606941600000,
   "live":False,
   "awayTeamFirst":True,
   "denySameGame":"NO",
   "teaserAllowed":True,
   "competitionId":"241",
   "notes":"",
   "numMarkets":99,
   "lastModified":1606877221057,
   "competitors":[
      {
         "id":"7995252-11904223",
         "name":"Pittsburgh Steelers",
         "home":True
      },
      {
         "id":"7995252-11903831",
         "name":"Baltimore Ravens",
         "home":False
      }
   ],
   "displayGroups":[
      {
         "id":"100-41",
         "description":"Game Lines",
         "defaultType":True,
         "alternateType":False,
         "markets":[
            {
               "id":"135743251",
               "descriptionKey":"Main Dynamic Asian Handicap",
               "description":"Point Spread",
               "key":"2W-HCAP",
               "marketTypeId":"120718",
               "status":"O",
               "singleOnly":False,
               "notes":"",
               "period":{
                  "id":"119",
                  "description":"Game",
                  "abbreviation":"G",
                  "live":False,
                  "main":True
               },
               "outcomes":[
                  {
                     "id":"731459408",
                     "description":"Baltimore Ravens",
                     "status":"O",
                     "type":"A",
                     "competitorId":"7995252-11903831",
                     "price":{
                        "id":"6649403897",
                        "handicap":"10.0",
                        "american":"-110",
                        "decimal":"1.909091",
                        "fractional":"10/11",
                        "malay":"0.91",
                        "indonesian":"-1.10",
                        "hongkong":"0.91"
                     }
                  },
                  {
                     "id":"731459409",
                     "description":"Pittsburgh Steelers",
                     "status":"O",
                     "type":"H",
                     "competitorId":"7995252-11904223",
                     "price":{
                        "id":"6649403896",
                        "handicap":"-10.0",
                        "american":"-110",
                        "decimal":"1.909091",
                        "fractional":"10/11",
                        "malay":"0.91",
                        "indonesian":"-1.10",
                        "hongkong":"0.91"
                     }
                  }
               ]
            },
            {
               "id":"135743218",
               "descriptionKey":"Head To Head",
               "description":"Moneyline",
               "key":"2W-12",
               "marketTypeId":"11",
               "status":"O",
               "singleOnly":False,
               "notes":"",
               "period":{
                  "id":"119",
                  "description":"Game",
                  "abbreviation":"G",
                  "live":False,
                  "main":True
               },
               "outcomes":[
                  {
                     "id":"731459382",
                     "description":"Baltimore Ravens",
                     "status":"O",
                     "type":"A",
                     "competitorId":"7995252-11903831",
                     "price":{
                        "id":"6647384558",
                        "american":"+350",
                        "decimal":"4.50",
                        "fractional":"7/2",
                        "malay":"-0.29",
                        "indonesian":"3.50",
                        "hongkong":"3.50"
                     }
                  },
                  {
                     "id":"731459383",
                     "description":"Pittsburgh Steelers",
                     "status":"O",
                     "type":"H",
                     "competitorId":"7995252-11904223",
                     "price":{
                        "id":"6647384557",
                        "american":"-500",
                        "decimal":"1.200",
                        "fractional":"1/5",
                        "malay":"0.20",
                        "indonesian":"-5.00",
                        "hongkong":"0.20"
                     }
                  }
               ]
            },
            {
               "id":"135743239",
               "descriptionKey":"Main Dynamic Over/Under",
               "description":"Total",
               "key":"2W-OU",
               "marketTypeId":"120717",
               "status":"O",
               "singleOnly":False,
               "notes":"",
               "period":{
                  "id":"119",
                  "description":"Game",
                  "abbreviation":"G",
                  "live":False,
                  "main":True
               },
               "outcomes":[
                  {
                     "id":"731459394",
                     "description":"Over",
                     "status":"O",
                     "type":"O",
                     "price":{
                        "id":"6648228928",
                        "handicap":"42.0",
                        "american":"-110",
                        "decimal":"1.909091",
                        "fractional":"10/11",
                        "malay":"0.91",
                        "indonesian":"-1.10",
                        "hongkong":"0.91"
                     }
                  },
                  {
                     "id":"731459395",
                     "description":"Under",
                     "status":"O",
                     "type":"U",
                     "price":{
                        "id":"6648228927",
                        "handicap":"42.0",
                        "american":"-110",
                        "decimal":"1.909091",
                        "fractional":"10/11",
                        "malay":"0.91",
                        "indonesian":"-1.10",
                        "hongkong":"0.91"
                     }
                  }
               ]
            }
         ],
         "order":1
      }
   ]
}
"""
