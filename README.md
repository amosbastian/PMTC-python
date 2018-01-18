Post-Match Thread Creator
====================

This code is used to parse match history links from the game League of Legends and output text that can be used to create post-match threads on Reddit.

Installation
--------------------
To install this program simply clone the repository

```bash
git clone https://github.com/amosbastian/mhp.git
```
Usage
--------------------
Once cloned you can simply run the program with Python (works with Python 2.7, 3.3, 3.4, 3.5, and 3.6), using the match history's URL as a command line argument.

Usage example:

```
cd pmc
python pmc.py "https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/550247?gameHash=e8da58c50577df24&tab=overview"
```

with output

```
||**Bans 1**|**Bans 2**|[G](#mt-gold)|[vs](#mt-kills)|[T](#mt-towers)|**Objectives**
|:--|:--:|:--:|:--:|:--:|:--:|:--:|
|KSV|[tahmkench](#c-tahmkench) [kogmaw](#c-kogmaw) [azir](#c-azir)|[khazix](#c-khazix) [jarvaniv](#c-jarvaniv)|70.92k|11|11|[H](#mt-herald)^1 [B](#mt-barons)^4 [M](#mt-mountain)^5|
|KZ|[kalista](#c-kalista) [sejuani](#c-sejuani) [shen](#c-shen)|[janna](#c-janna) [alistar](#c-alistar)|61.08k|8|2|[C](#mt-cloud)^2 [M](#mt-mountain)^3|

|**KSV**|11-8-26|[vs](#mt-kills)|8-11-14|**KZ**|
|--:|--:|:--:|:--|:--|
|CuVee [gangplank](#c-gangplank)|5-2-4|TOP|6-2-0|[vladimir](#c-vladimir) Rascal|
|Ambition [rengar](#c-rengar)|2-4-2|JNG|0-3-7|[leesin](#c-leesin) Peanut|
|Crown [malzahar](#c-malzahar)|2-2-6|MID|2-1-2|[ryze](#c-ryze) Bdd|
|Ruler [ezreal](#c-ezreal)|2-0-6|ADC|0-4-2|[sivir](#c-sivir) PraY|
|CoreJJ [braum](#c-braum)|0-0-8|SUP|0-1-3|[taric](#c-taric) GorillA|
```

What can I use this for?
--------------------
If you want to create a post-match thread on [/r/LeagueOfLegends](https://www.reddit.com/r/leagueoflegends/) and you are too lazy to manually enter everything like me, then use this! The gif below shows how easy this is!

![](https://i.imgur.com/Icl9ACw.gif)
