import json
import requests
import sys

API_BASE_URL = "https://acs.leagueoflegends.com/v1/stats/game/TRLH3/{}"

class Player(object):
    def __init__(self, player_id, win, kills, deaths, assists, gold_earned):
        self.id = player_id
        self.win = win
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.gold_earned = gold_earned

def create_player(obj):
        return Player(obj["participantId"], obj["win"], obj["kills"],
            obj["deaths"], obj["assists"], obj["goldEarned"])


def team_split(players):
    team_1 = players[0]["player"]["summonerName"].split()[0]
    team_2 = players[5]["player"]["summonerName"].split()[0]
    return team_1, team_2

if __name__ == '__main__':
    match_history = sys.argv[1].split("/")[-1]
    request = requests.get(API_BASE_URL.format(match_history)).json()
    players = request["participants"]
    game_duration = round(request["gameDuration"] / 60)
    teams = request["teams"]

    player_objects = [create_player(player["stats"]) for player in players]

    for player in player_objects:
        print("{} {}-{}-{}".format(player.id, player.kills, player.deaths,
            player.assists))