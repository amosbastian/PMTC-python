import json
import requests
from bs4 import BeautifulSoup
import re

def get_response(url):
    """
    Gets the response from the given URL with some error checking.
    """
    if not "www.over.gg" in url:
        sys.exit("Please enter a URL from www.hltv.org.")
    try:
        response = requests.get(url)
        return response
    except Exception as error:
        sys.exit("{}: Please enter a valid URL.".format(repr(error)))

if __name__ == '__main__':
    url = "https://www.over.gg/6470/phl-vs-gla-overwatch-league-season-1-stage-1-w2"
    response = get_response(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    game_wrappers = soup.find_all("div", {"class" : "game-wrapper"})
    teams = game_wrappers[0].find_all("div", {"class" : "game-team"})
    team_1_players = teams[0].find_all("a", {"class", "game-team-player"})
    players_1 = [player.text for player in team_1_players]
    for player in players_1:
        print(re.sub(r"\s+", "", player))