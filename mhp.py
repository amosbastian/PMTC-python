import json
import requests
import sys

API_BASE_URL = "https://acs.leagueoflegends.com/v1/stats/game/TRLH3/{}"
CHAMPION_URL = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"

# /r/LeagueOfLegends
VS = "[vs](#mt-kills)"
GOLD = "[G](#mt-gold)"
TOWERS = "[T](#mt-towers)"

class Player(object):
    """A player participating in a League of Legends match."""
    def __init__(self, player_id, win, kills, deaths, assists, gold_earned,
        champion, name, team):

        self.assists = assists
        self.champion = champion
        self.deaths = deaths
        self.gold_earned = gold_earned
        self.id = player_id
        self.kills = kills
        self.name = name
        self.position = self.get_position(self.id)
        self.team = team
        self.win = win

    def get_position(self, player_id):
        """ Gets the player's position depending on their player_id."""
        if player_id == 1 or player_id == 6:
            return "TOP"
        elif player_id == 2 or player_id == 7:
            return "JNG"
        elif player_id == 3 or player_id == 8:
            return "MID"
        elif player_id == 4 or player_id == 9:
            return "ADC"
        else:
            return "SUP"

def champion_dictionary(obj):
    """Converts champion.json to a dictionary that is useful to us."""
    champions = {}
    for champion in obj["data"]:
        name = champion.lower()
        champions[int(obj["data"][champion]["key"])] = name
    return champions

def create_player(player_info, obj):
    """ Creates a Player object out of the given information and obj."""
    stats = obj["stats"]
    player = player_info[stats["participantId"] - 1]["player"]
    team = player["summonerName"].split()[0]
    name = player["summonerName"].split()[1]
    return Player(stats["participantId"], stats["win"], stats["kills"],
        stats["deaths"], stats["assists"], stats["goldEarned"],
        obj["championId"], name, team)

def team_kda(players):
    kills = sum([player.kills for player in players])
    deaths = sum([player.deaths for player in players])
    assists = sum([player.assists for player in players])

    return "{}-{}-{}".format(kills, deaths, assists)

def champion_converter(champion_id):
    champion_id = "{}".format(champion_id)
    if champion_id in champions:
        champion = champions[champion_id]
    else:
        champion = champion_id
    return "[{}](#c-{})".format(champion, champion)

def team_split(players):
    team_1 = players[0]["player"]["summonerName"].split()[0]
    team_2 = players[5]["player"]["summonerName"].split()[0]
    return team_1, team_2

def print_scoreboard():
    print("|**{}**|{}|{}|{}|**{}**|".format(team_1_short, team_1_kda, VS,
        team_2_kda, team_2_short))
    print("|--:|--:|:--:|:--|:--|")
    for player_1, player_2 in zip(players_1, players_2):
        print("|{} {}|{}-{}-{}|{}|{}-{}-{}|{} {}|".format(
            player_1.name, champion_converter(player_1.champion),
            player_1.kills, player_1.deaths, player_1.assists,
            player_1.position, player_2.kills, player_2.deaths,
            player_2.assists, champion_converter(player_2.champion),
            player_2.name
            ))

if __name__ == '__main__':
    # match_history = sys.argv[1].split("/")[-1]
    match_history = "1002320090?gameHash=a534cb383e6b49dc&tab=overview"
    with open("champion.json", "r") as json_data:
        champions = json.load(json_data)

    request = requests.get(API_BASE_URL.format(match_history)).json()
    players = request["participants"]
    game_duration = round(request["gameDuration"] / 60)
    teams = request["teams"]

    player_info = request["participantIdentities"]
    player_objects = [create_player(player_info, player) for player in players]

    players_1 = player_objects[:5]
    players_2 = player_objects[5:]

    team_1_kda = team_kda(players_1)
    team_1_short = players_1[0].team
    team_2_kda = team_kda(players_2)
    team_2_short = players_2[0].team

    print_scoreboard()