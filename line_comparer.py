import re
from bovada_scraper import *
from sportsplays_scraper import *
LINE_THRESHOLDS = {
    "moneyline" : .01
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
    if not bv_moneyline or not sp_moneyline:
        return
    for team in teams:
        if team in sp_moneyline and team in bv_moneyline:
            if sp_moneyline[team]["price"] != None and bv_game['moneyline'][team]["price"] != None:
                sp_price = convert_price_to_decimal(sp_game['moneyline'][team]["price"])
                bv_price = convert_price_to_decimal(bv_game['moneyline'][team]["price"])
                percent_diff = (sp_price - bv_price)/bv_price
                if  percent_diff > LINE_THRESHOLDS["moneyline"]:
                    profitable_moneyline_bets.append(
                        {
                            "Sport": sport,
                            "Period": period,
                            "Date": sp_game["date"], 
                            "Game": "{} vs {}".format(sp_game['teams'][0],sp_game['teams'][1]), 
                            "Bet": team, 
                            "Juice": round(percent_diff, 5),
                            "SP Price": round(sp_price, 5),
                            "BV Price": round(bv_price, 5)
                        }
                    )
        
def compare_lines(sportplays_lines, bovada_lines, sport, period):
    bv_line = bovada_lines[period]
    sp_line = sportplays_lines[period]
    not_matched = []
    profitable_moneyline_bets = []
    # first try to find match through team name
    for sp_game in sp_line:
        matched = False
        for bv_game in bv_line:
            if bv_game['teams'][0] in sp_game['teams'] and bv_game['teams'][1] in sp_game['teams']\
                                                        and bv_game['date'] == sp_game['date']:
                compare_matched_money_line(bv_game, sp_game, profitable_moneyline_bets, sport, period)
                matched = True
                break
        # might have to deal with case where team names don't exactly match
        if not matched:
            not_matched.append(sp_game)
    print("Unmatched Lines: {}/{}".format(len(not_matched),len(sp_line) - len(not_matched)))
    print_game_detail(not_matched)
    return profitable_moneyline_bets

def print_game_detail(lines):
    for line in lines:
        print("{} vs {} on {}".format(line['teams'][0], line['teams'][1], line["date"]))

def compare_nfl_lines(session):
    periods = ["Total Game"]
    bv_data = nfl_bv_scraper()
    sp_data = nfl_sp_scraper(session)
    profitable_bets = []
    for period in periods:
        profitable_bets.extend(compare_lines(sp_data, bv_data, 'NFL', period))
    return profitable_bets

def compare_soccer_lines(session):
    periods = ["Total Game"]
    bv_data = nfl_bv_scraper()
    sp_data = nfl_sp_scraper(session)
    profitable_bets = []
    for period in periods:
        profitable_bets.extend(compare_lines(sp_data, bv_data, 'SOC', period))
    return profitable_bets