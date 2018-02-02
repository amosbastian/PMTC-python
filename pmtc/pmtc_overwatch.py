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

class Match(object):
    def __init__(self, map_id, match):
        self.id = map_id
        self.match = match
        self.team_1_players = self.players(0)
        self.team_2_players = self.players(1)
        self.team_1_name = self.team_name(0)
        self.team_2_name = self.team_name(1)
        self.team_1_short = self.team_1_name.split(" ")[-1]
        self.team_2_short = self.team_2_name.split(" ")[-1]

    @property
    def teams(self):
        return self.match.find_all("div", {"class" : "game-team"})

    @property
    def game(self):
        return self.match.find_all("div", {"class" : "game-stats-team"})

    def players(self, team_id):
        team = self.teams[team_id]
        players = team.find_all("a", {"class", "game-team-player"})
        return [re.sub(r"\s+", "", player.text) for player in players]

    def team_name(self, team_id):
        team = self.game[team_id]
        name = team.find("div", {"class" : "game-stats-team-name"})
        return name.text.split("\t")[2]

if __name__ == '__main__':
    url = "https://www.over.gg/6470/phl-vs-gla-overwatch-league-season-1-stage-1-w2"
    response = get_response(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    matches = soup.find_all("div", {"class" : "game-wrapper"})
    game = matches[0].find_all("div", {"class" : "game-stats-team"})
    print(game[1].find("div", {"class" : "game-stats-team-name"}).text.split("\t"))
    for i, match in enumerate(matches):
        match = Match(i, match)
        print(match.team_1_name + " vs. " + match.team_2_name)
        print(match.team_1_short + " vs. " + match.team_2_short)