import requests
from bs4 import BeautifulSoup
from collections import namedtuple

def create_players(table):
    team_data = []
    Player = namedtuple("Player", 
        ["name", "k", "a", "d", "kast", "kddiff", "adr", "fkdiff", "rating"])

    for i, row in enumerate(table.select("tr")):
        if i == 2:
            print(table.select("tr").find_all("td"))

    for i, row in enumerate(table.select("tr")):
        if i > 0:
            player_row = row.find_all("td")
            player = [player.text for player in player_row]
            team_data.append(Player(*player))
    return team_data

def team_logo(team):
    return "[](#{}-logo)".format(team.lower())

if __name__ == '__main__':
    response = requests.get("https://www.hltv.org/stats/matches/mapstatsid/59934/g2-vs-cloud9")
    soup = BeautifulSoup(response.text, "lxml")
    
    Team = namedtuple("Team", ["name", "players"])
    
    stats_tables = soup.find_all("table", {"class" : "stats-table"})
    
    table_1 = stats_tables[0]
    # print(table_1)
    table_2 = stats_tables[1]

    team = Team(table_1.find_all("th")[0].text, create_players(table_1))
    # team_2 = Team(table_2.find_all("th")[0].text, create_players(table_2))

    # print("|{} **{}**|**K**|**A**|**D**|**Rating**|".format(
    #     team_logo(team.name), team.name))
    # print("|:--|:--:|:--:|:--:|:--:|")
