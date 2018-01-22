Post-Match Thread Creator
====================

Code in this repository can be used to parse match history links from the game League of Legends or HLTV links for the game Counter-Strike: Global Offensive and output text that can be used to create post-match threads on Reddit.

Installation
--------------------
To install this program simply clone the repository

```bash
git clone https://github.com/amosbastian/mhp.git
```
Usage
--------------------
Once cloned you can simply run the program you want to use with with Python (works with Python 2.7, 3.3, 3.4, 3.5, and 3.6), using the match history's URL or HLTV URL as a command line argument.

#### League of Legends

```
cd PMTC/pmtc
python pmtc_lol.py "https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT06/550247?gameHash=e8da58c50577df24&tab=overview"
```

with outputs

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

#### Counter-Strike: Global Offensive

```
python pmtc_csgo.py https://www.hltv.org/stats/matches/mapstatsid/59934/g2-vs-cloud9
```

which outputs

```
&nbsp;

###MAP: 

&nbsp;

|Team|T|CT|Total|
|:--|:--:|:--:|:--:|
|[](#cloud9-logo)|5|3|8|
|[](#g2-logo)|10|6|16|

&nbsp;

|[](#cloud9-logo) **C9**|**K**|**A**|**D**|**Rating**|
|:--|:--:|:--:|:--:|:--:|
|[](#lang-us) tarik|26|5|17|1.55|
|[](#lang-us) RUSH|14|2|19|0.88|
|[](#lang-us) Stewie2K|13|5|18|0.86|
|[](#lang-us) autimatic|13|6|19|0.76|
|[](#lang-us) Skadoodle|6|6|19|0.61|
|[](#g2-logo) **G2**|
|[](#lang-fr) NBK-|27|3|13|1.59|
|[](#lang-fr) apEX|17|5|15|1.24|
|[](#lang-fr) kennyS|17|6|13|1.18|
|[](#lang-fr) shox|19|3|14|1.15|
|[](#lang-fr) bodyy|12|5|17|0.91|

```

What can I use this for?
--------------------
If you want to create a post-match thread on [/r/LeagueOfLegends](https://www.reddit.com/r/leagueoflegends/) or [/r/GlobalOffensive/](https://www.reddit.com/r/GlobalOffensive) and you are too lazy to manually enter everything like me, then use this! The gif below shows how easy this is!

![](https://i.imgur.com/ThMJrOJ.gif)
