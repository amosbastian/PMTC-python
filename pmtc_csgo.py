import json
import pycountry
import requests
import sys

from bs4 import BeautifulSoup
from collections import namedtuple

def create_players(table):
    """
    Loop through given table and create Player objects with the following
    attributes:
        - Nationality
        - Name
        - Kills
        - Assists
        - Deaths
        - KAST
        - K/D Diff
        - ADR
        - FK Diff
        - Rating
    """
    team_data = []
    Player = namedtuple("Player", ["name", "k", "a", "d", "kast", "kddiff",
        "adr", "fkdiff", "rating", "nationality"])

    for i, row in enumerate(table.select("tr")):
        if i > 0:
            player_row = row.find_all("td")
            nationality = player_row[0].find("img").get("alt", "")
            player = [player.text for player in player_row]
            player.append(nationality)
            team_data.append(Player(*player))
    return team_data

def team_logo(team, white=True):
    """
    Takes a team's name and (hopefully) converts it to a team's logo on Reddit.
    """
    if white:
        return "[](#{}w-logo)".format(team.lower())
    else:
        return "[](#{}-logo)".format(team.lower())

def country_converter(country):
    if country == "Russia":
        return "ru"
    elif country == "Czech Republic":
        return "cz"

def print_scoreboard(team):
    """
    Prints the scoreboard of the given team.
    """
    for player in team.players:
        try:
            nat = pycountry.countries.get(name=player.nationality).alpha_2
        except Exception as error:
            nat = country_converter(player.nationality)

        print("|[](#lang-{}) {}|{}|{}|{}|{}|".format(nat.lower(),
            player.name, player.k.split()[0], player.a.split()[0],
            player.d.split()[0], player.rating))

def create_post(team_1, team_2):
    """
    Prints the entire scoreboard for both teams.
    """
    logo = teams[team_1.name]["logo"]
    print("|{} **{}**|**K**|**A**|**D**|**Rating**|".format(team_logo(logo),
        team_1.name))
    print("|:--|:--:|:--:|:--:|:--:|")
    print_scoreboard(team_1)

    logo = teams[team_2.name]["logo"]
    print("|{} **{}**|".format(team_logo(logo, False), team_2.name))
    print_scoreboard(team_2)

if __name__ == '__main__':
    url = str(sys.argv[1])
    if not "www.hltv.org" in url:
        print("Please enter a URL from www.hltv.org.")

    try:
        response = requests.get(url)
    except Exception as error:
        sys.exit("{}: Please enter a valid URL.".format(repr(error)))

    with open("csgo.json", "r") as json_data:
        teams = json.load(json_data)

    soup = BeautifulSoup(response.text, "lxml")
    Team = namedtuple("Team", ["name", "players"])
    
    stats_tables = soup.find_all("table", {"class" : "stats-table"})

    try:
        table_1 = stats_tables[0]
        table_2 = stats_tables[1]

        team_1 = Team(table_1.find_all("th")[0].text, create_players(table_1))
        team_2 = Team(table_2.find_all("th")[0].text, create_players(table_2))
        create_post(team_1, team_2)
    except Exception as error:
        print("Please enter a URL from the detailed stats page.")