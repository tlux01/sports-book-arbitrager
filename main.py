import threading
import time
from line_comparer import *
from sportsplays_scraper import create_sportsplays_session
from exceptions import InvalidSessionError
from email_service import generate_message_for_profitable_bets, send_email_message
def run():
    session = create_sportsplays_session()
    num_error = 0
    while True:
        if num_error == 3:
            print("Please investigate session login failure")
            break
        prof = []
        try:
            prof.extend(compare_nfl_lines(session))
            prof.extend(compare_soccer_lines(session))
            prof.extend(compare_nba_lines(session))
            html = generate_message_for_profitable_bets(prof)
            send_email_message("Profitable Bets", html)
            num_error = 0
        except InvalidSessionError:
            print("Session Invalid, retrying")
            # create new session
            session = create_sportsplays_session()
            num_error += 1
        
        time.sleep(60*30)

if __name__ == '__main__':
    run()

