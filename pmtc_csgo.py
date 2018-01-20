import pycountry
import requests
import sys

from bs4 import BeautifulSoup
from collections import namedtuple

def create_players(table):
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

def team_logo(team):
    return "[](#{}-logo)".format(team.lower())

def print_scoreboard(team):
    for player in team.players:
        nationality = pycountry.countries.get(name=player.nationality).alpha_2
        print("|[](#lang-{}) {}|{}|{}|{}|{}|".format(nationality.lower(),
            player.name, player.k.split()[0], player.a.split()[0],
            player.d.split()[0], player.rating))

def create_post(team_1, team_2):
    print("|{} **{}**|**K**|**A**|**D**|**Rating**|".format(
        team_logo(team_1.name), team_1.name))
    print("|:--|:--:|:--:|:--:|:--:|")
    print_scoreboard(team_1)
    print("|{} **{}**|".format(team_logo(team_2.name), team_2.name))
    print_scoreboard(team_2)

if __name__ == '__main__':
    url = str(sys.argv[1])
    if not "www.hltv.org" in url:
        print("Please enter a URL from www.hltv.org.")

    try:
        response = requests.get(url)
    except Exception as error:
        sys.exit("{}: Please enter a valid URL.".format(repr(error)))

    soup = BeautifulSoup(response.text, "lxml")
    
    Team = namedtuple("Team", ["name", "players"])
    
    stats_tables = soup.find_all("table", {"class" : "stats-table"})
    
    table_1 = stats_tables[0]
    # print(table_1)
    table_2 = stats_tables[1]

    team_1 = Team(table_1.find_all("th")[0].text, create_players(table_1))
    team_2 = Team(table_2.find_all("th")[0].text, create_players(table_2))
    create_post(team_1, team_2)

    print()