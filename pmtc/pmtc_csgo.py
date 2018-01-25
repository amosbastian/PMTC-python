import json
import pycountry
import requests
import sys
import os

from bs4 import BeautifulSoup
from collections import namedtuple

directory = os.path.dirname(os.path.abspath(__file__))

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
    if white and teams[team.name]["white"]:
        return "[](#{}w-logo)".format(team.logo.lower())
    else:
        return "[](#{}-logo)".format(team.logo.lower())

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

def print_overview(team_1, team_2):
    """
    Prints the overview of the match.
    """
    print("|Team|T|CT|Total|\n|:--|:--:|:--:|:--:|")
    print("|{}|{}|{}|{}|".format(team_logo(team_1, False),
        team_1.match.first, team_1.match.second,
        team_1.match.first + team_1.match.second))
    print("|{}|{}|{}|{}|".format(team_logo(team_2, False),
        team_2.match.first, team_2.match.second,
        team_2.match.first + team_2.match.second))
    print("\n&nbsp;\n")

def create_post(team_1, team_2):
    """
    Prints the entire scoreboard for both teams.
    """
    print("\n&nbsp;\n\n###MAP: \n\n&nbsp;\n")
    print_overview(team_1, team_2)
    print("|{} **{}**|**K**|**A**|**D**|**Rating**|".format(
        team_logo(team_1), team_1.initials))
    print("|:--|:--:|:--:|:--:|:--:|")
    print_scoreboard(team_1)
    print("|{} **{}**|".format(team_logo(team_2, False), team_2.initials))
    print_scoreboard(team_2)

def count_rounds(half):
    """
    Counts how many rounds were won in the half.
    """
    rounds = 0
    for img in half.find_all("img"):
        if not "emptyHistory.svg" in img["src"]:
            rounds += 1
    return rounds

def team_match(team=1):
    """
    Creates a Match object with how many matches the team won in each half.
    """
    Match = namedtuple("Match", ["first", "second"])

    halves = soup.find_all("div", {"class" : "round-history-half"})
    if team == 1:
        first_half = halves[0]
        second_half = halves[1]
    else:
        first_half = halves[2]
        second_half = halves[3]

    Match.first = count_rounds(first_half)
    Match.second = count_rounds(second_half)
    return Match

def get_response(url):
    """
    Gets the response from the given URL with some error checking.
    """
    if not "www.hltv.org" in url:
        sys.exit("Please enter a URL from www.hltv.org.")
    try:
        response = requests.get(url)
        return response
    except Exception as error:
        sys.exit("{}: Please enter a valid URL.".format(repr(error)))

if __name__ == '__main__':
    url = str(sys.argv[1])
    response = get_response(url)

    with open("{}/csgo.json".format(directory), "r") as json_data:
        teams = json.load(json_data)

    soup = BeautifulSoup(response.text, "lxml")
    Team = namedtuple("Team", ["name", "players", "match", "logo", "initials"])
    
    stats_tables = soup.find_all("table", {"class" : "stats-table"})

    table_1 = stats_tables[0]
    table_2 = stats_tables[1]
    name_1 = table_1.find_all("th")[0].text
    name_2 = table_2.find_all("th")[0].text

    team_1 = Team(name_1, create_players(table_1), team_match(1),
        teams[name_1]["logo"], teams[name_1]["name"])
    team_2 = Team(name_2, create_players(table_2), team_match(2),
        teams[name_2]["logo"], teams[name_2]["name"])
    create_post(team_1, team_2)