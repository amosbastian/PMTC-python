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
    def __init__(self, map_id, match, match_map):
        self.id = map_id
        self.match = match
        self.map = match_map
        self.team_1_players = self.players(0)
        self.team_2_players = self.players(1)
        self.team_1_name = self.team_name(0)
        self.team_2_name = self.team_name(1)
        self.team_1_short = self.team_1_name.split(" ")[-1]
        self.team_2_short = self.team_2_name.split(" ")[-1]
        self.team_1_score = self.game_score(0)
        self.team_2_score = self.game_score(1)

    @property
    def teams(self):
        """All information about the players"""
        return self.match.find_all("div", {"class" : "game-team"})

    @property
    def game(self):
        """All information about the game"""
        return self.match.find_all("div", {"class" : "game-stats-team"})

    def players(self, team_id):
        """Returns the players of the team with the given team_id"""
        team = self.teams[team_id]
        players = team.find_all("a", {"class", "game-team-player"})
        return [re.sub(r"\s+", "", player.text) for player in players]

    def team_name(self, team_id):
        """Returns the name of the team with the given team_id"""
        team = self.game[team_id]
        name = team.find("div", {"class" : "game-stats-team-name"})
        name = name.text.split()
        if "Winner" in name:
            name.remove("Winner")
            self.winner = " ".join(name)

        name = " ".join(name)
        return name

    @property
    def game_type(self):
        g_ = self.game[0].find_all("span", {"class" : "game-stats-team-label"})
        return [game.text[:-2] for game in g_]

    def game_score(self, team_id):
        g_ = self.game[team_id].find_all("span", 
            {"class" : "game-stats-team-value"})
        return [game.text.strip() for game in g_]

    @property
    def mode(self):
        if self.id == 0:
            return "Hybrid"
        elif self.id == 1:
            return "Assault"
        elif self.id == 2:
            return "Control"
        elif self.id == 3:
            return "Escort"
        else:
            return "Control"


def print_match(match, total):
    if not match.id == 0:
        print("\n")
    print("---\n\n###MAP {}/{}: {}".format(match.id + 1, total, match.map))
    print("\n**Winner:** {}\n".format(match.winner))
    print("||{}|*{}*|{}||\n|--:|--:|:--:|:--|:--|".format(match.team_1_short,
        match.mode, match.team_2_short))
    for i in range(6):
        if i < len(match.team_1_score):
            print("|{}|{}|{}|{}|{}|".format(match.team_1_players[i],
                match.team_1_score[i], match.game_type[i],
                match.team_2_score[i], match.team_2_players[i]))
        else:
            print("|{}||||{}|".format(match.team_1_players[i],
                match.team_2_players[i]))
        
    if match.id + 1 == total:
        print("\n---")

def create_post(matches):
    for match in matches:
        print_match(match, len(matches))

if __name__ == '__main__':
    url = "https://www.over.gg/6470/phl-vs-gla-overwatch-league-season-1-stage-1-w2"
    response = get_response(url)
    soup = BeautifulSoup(response.text, "lxml")
    maps = soup.find_all("div", {"class" : "game-switch-map-name"})
    maps = [" ".join(map_.text.split()) for map_ in maps]
    matches = soup.find_all("div", {"class" : "game-wrapper"})

    matches = [Match(i, match, maps[i]) for i, match in enumerate(matches)]
    create_post(matches)