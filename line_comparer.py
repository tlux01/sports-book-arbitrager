import re
from bovada_scraper import *
from sportsplays_scraper import *
LINE_THRESHOLDS = {
    "moneyline" : .25
}

def convert_price_to_decimal(line):
    if line == None:
        return None
    elif line == 'EVEN':
        return 1
    elif "-" in line:
        return 100/(int(line)*-1)
    else:
        return int(line)/100

def compare_matched_money_line(sp_game, bv_game, profitable_moneyline_bets, sport, period):
    teams = sp_game["teams"]
    sp_moneyline = sp_game["moneyline"]
    bv_moneyline = bv_game["moneyline"]
    for team in teams:
        if team in sp_moneyline and team in bv_moneyline:
            if sp_moneyline[team]["price"] != None and bv_game['moneyline'][team]["price"] != None:
                sp_price = convert_price_to_decimal(sp_game['moneyline'][team]["price"])
                bv_price = convert_price_to_decimal(bv_game['moneyline'][team]["price"])
                if sp_price - bv_price > LINE_THRESHOLDS["moneyline"]:
                    profitable_moneyline_bets.append(
                        {
                            "sport": sport,
                            "period": period,
                            "game": sp_game['teams'], 
                            "team": team, 
                            "date": sp_game["date"], 
                            "SP Price": sp_price, 
                            "BV Price": bv_price
                        }
                    )
        
def compare_lines(sportplays_lines, bovada_lines, sport):
    period = "Total Game"
    bv_line = bovada_lines[period]
    sp_line = sportplays_lines[period]
    not_matched = []
    profitable_moneyline_bets = []
    # first try to find match through team name
    for sp_game in sp_line:
        matched = False
        for bv_game in bv_line:
            if bv_game['teams'][0] in sp_game['teams'] and bv_game['teams'][1] in sp_game['teams']:
                compare_matched_money_line(bv_game, sp_game, profitable_moneyline_bets, sport, period)
                matched = True
                break
        # might have to deal with case where team names don't exactly match
        if not matched:
            not_matched.append(sp_game)
    print("Unmatched Lines: {}".format(len(not_matched)))
    print("Matched Lines: {}".format(len(sp_line) - len(not_matched)))
    return profitable_moneyline_bets
print(compare_lines(nfl_sp_scraper(session), nfl_bv_scraper(),  "NFL"))
print(compare_lines(soccer_sp_scraper(session), soccer_bv_scraper(),"SOC"))