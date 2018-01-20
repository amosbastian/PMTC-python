import json
import requests
import sys

API_BASE_URL = "https://acs.leagueoflegends.com/v1/stats/game/"

# /r/LeagueOfLegends stuff
VS = "[vs](#mt-kills)"
GOLD = "[G](#mt-gold)"
TOWERS = "[T](#mt-towers)"

class Player(object):
    """A player participating in a League of Legends match."""
    def __init__(self, player_id, win, kills, deaths, assists, gold,
        champion, name, team):

        self.assists = assists
        self.champion = champion
        self.deaths = deaths
        self.gold = gold
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
    """Creates a Player object out of the given information and obj."""
    stats = obj["stats"]
    player = player_info[stats["participantId"] - 1]["player"]
    team = player["summonerName"].split()[0]
    name = player["summonerName"].split()[1]
    return Player(stats["participantId"], stats["win"], stats["kills"],
        stats["deaths"], stats["assists"], stats["goldEarned"],
        obj["championId"], name, team)

def team_kda(players):
    """Calculates the team's KDA from the KDA of its players."""
    kills = sum([player.kills for player in players])
    deaths = sum([player.deaths for player in players])
    assists = sum([player.assists for player in players])

    return "{}-{}-{}".format(kills, deaths, assists)

def champion_converter(champion_id):
    """
    Converts champion_id to a string format that shows champion's portrait on 
    Reddit.
    """
    champion_id = "{}".format(champion_id)
    if champion_id in champions:
        champion = champions[champion_id]
    else:
        champion = champion_id
    return "[{}](#c-{})".format(champion, champion)

def print_scoreboard():
    """Prints the scoreboard used to create a post-match thread on Reddit."""
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

def get_events(url):
    """
    Gets all events of the given match. Events we are interested in:
        - Rift Herald
        - Cloud Dragon
        - Mountain Dragon
        - Ocean dragon
        - Infernal dragon
        - Baron Nashor
    """
    response = requests.get(url).json()

    events = []
    for frame in response["frames"]:
        for event in frame["events"]:
            if event["type"] == "ELITE_MONSTER_KILL":
                events.append(event)

    return events

def event_converter(event):
    """
    Converts event to string format that shows the event's portait on Reddit.
    """
    if event["monsterType"] == "DRAGON":
        event = event["monsterSubType"]
    else:
        event = event["monsterType"]

    if event == "BARON_NASHOR":
        return "[B](#mt-barons)"
    elif event == "RIFTHERALD":
        return "[H](#mt-herald)"
    elif event == "FIRE_DRAGON":
        return "[I](#mt-infernal)"
    elif event == "EARTH_DRAGON":
        return "[M](#mt-mountain)"
    elif event == "WATER_DRAGON":
        return "[O](#mt-ocean)"
    else:
        return "[C](#mt-cloud)"

def split_events(events):
    """
    Split the events over each team. If the person who killed the event has an
    id less than or equal to five, then he is part of team 1, otherwise team 2.
    """
    objectives = [[], []]
    for i, event in enumerate(events):
        if event["killerId"] <= 5:
            objectives[0].append("{}^{}".format(event_converter(event), i + 1))
        else:
            objectives[1].append("{}^{}".format(event_converter(event), i + 1))

    return objectives

def ban_list(bans, team):
    """
    Create a list of two lists containing the banned champions of a team in
    each of the two ban phases.
    """
    ban_list = [[], []]

    if team == 1:
        phase_1, phase_2 = 0, 1
    else:
        phase_1, phase_2 = 1, 0
    
    for ban in sorted(bans, key=lambda x: x["pickTurn"]):
        ban_turn = ban['pickTurn']
        champion = champion_converter(ban['championId'])
        if ban_turn % 2 != 0:
            ban_list[phase_1].append(champion)
        else:
            ban_list[phase_2].append(champion)

    return ban_list

def create_team(team):
    """Creates a team (see the class)."""
    bans = ban_list(teams[team - 1]["bans"], team=team)
    events = split_events(game_events)[team - 1]
    player_objects = [create_player(player_info, p) for p in player_list]

    if team == 1:
        players = player_objects[:5]
    else:
        players = player_objects[5:]

    kda = team_kda(players)
    short = players[0].team
    towers = teams[team - 1]["towerKills"]
    return Team(team, bans, players, kda, short, towers, events)

class Team(object):
    """
    A class representing a team in League of Legends.
    """
    def __init__(self, team_id, bans, players, kda, short, towers, events):
        self.id = team_id
        self.bans = bans
        self.players = players
        self.short = short
        self.kda = kda
        self.towers = towers
        self.events = events

    @property
    def gold(self):
        return sum([player.gold for player in self.players])

    @property
    def kills(self):
        return sum([player.kills for player in self.players])

def ban_section(team_1, team_2):
    """Prints the ban section used in a post-match thread."""
    print("||**Bans 1**|**Bans 2**|{}|{}|{}|**Objectives**".format(GOLD,
        VS, TOWERS))
    print("|:--|:--:|:--:|:--:|:--:|:--:|:--:|")
    print("|{}|{}|{}|{:.2f}k|{}|{}|{}|".format(team_1.short, 
        ' '.join(team_1.bans[0]), ' '.join(team_1.bans[1]),
        team_1.gold / 1000.0, team_1.kills, team_1.towers,
        ' '.join(team_1.events)))
    print("|{}|{}|{}|{:.2f}k|{}|{}|{}|\n".format(team_2.short, 
        ' '.join(team_2.bans[0]), ' '.join(team_2.bans[1]),
        team_2.gold / 1000.0, team_2.kills, team_2.towers,
        ' '.join(team_2.events)))

def scoreboard_section(team_1, team_2):
    """Prints the scoreboard section used in a post-match thread."""
    print("|**{}**|{}|{}|{}|**{}**|".format(team_1.short, team_1.kda, VS,
        team_2.kda, team_2.short))
    print("|--:|--:|:--:|:--|:--|")
    for p1, p2 in zip(team_1.players, team_2.players):
        print("|{} {}|{}-{}-{}|{}|{}-{}-{}|{} {}|".format(
            p1.name, champion_converter(p1.champion),
            p1.kills, p1.deaths, p1.assists,
            p1.position, p2.kills, p2.deaths,
            p2.assists, champion_converter(p2.champion),
            p2.name
            ))

def create_post(team_1, team_2):
    """
    Prints the ban section and scoreboard section used in a post-match thread.
    """
    ban_section(team_1, team_2)
    scoreboard_section(team_1, team_2)

if __name__ == '__main__':
    argument = sys.argv[1].split("/")
    match_history = argument[-1]
    region = argument[-2]
    match_id, match_hash = match_history.split("?gameHash=")

    with open("champion.json", "r") as json_data:
        champions = json.load(json_data)

    try:
        request = requests.get("{}{}/{}".format(API_BASE_URL, region,
            match_history)).json()
    except Exception as error:
        sys.exit("Please enter a valid match history URL.")

    # Get all the information needed to create the players and teams
    teams = request["teams"]
    player_list = request["participants"]
    player_info = request["participantIdentities"]
    game_events = get_events("{}{}/{}/timeline?gameHash={}".format(API_BASE_URL,
        region, match_id, match_hash))
    game_duration = round(request["gameDuration"] / 60)

    # Create the teams and create the post
    team_1 = create_team(1)
    team_2 = create_team(2)
    create_post(team_1, team_2)