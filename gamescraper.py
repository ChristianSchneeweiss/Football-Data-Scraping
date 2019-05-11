from bs4 import BeautifulSoup
from urllib.request import urlopen

from gameinfo import GameInfo


def desc_swapper(desc):
    if "Tore" in desc:
        return "goals"
    elif "Ballbesitz" in desc:
        return "possession %"
    elif "Schüsse aufs Tor" in desc:
        return "shots on target"
    elif "Schüsse neben das Tor" in desc:
        return "shots missing target"
    elif "Freistöße" in desc:
        return "freekicks"
    elif "Eckbälle" in desc:
        return "corners"
    elif "Abseits" in desc:
        return "offside"
    elif "Gehaltene Bälle" in desc:
        return "blocked"
    elif "Fouls" in desc:
        return "fouls"
    elif "Zweikämpfe" in desc:
        return "tackles %"
    elif "Pässe" in desc:
        return "passes %"
    elif "Gelbe Karten" in desc:
        return "yellow cards"
    elif "Platzverweise" in desc:
        return "red cards"
    return desc


def check_cast_to_float(stat):
    stat = stat.replace(",", ".")
    try:
        stat = float(stat)
        return stat
    except ValueError as e:
        return stat


def is_time_included(season_time):
    return len(season_time) >= 2


class GameScraper:
    def __init__(self, url):
        self.url = url
    
    def _get_html(self):
        html = urlopen(self.url)
        bs = BeautifulSoup(html.read(), "html.parser")
        return bs
    
    def scrape(self):
        bs = self._get_html()
        info = GameInfo()
        self.add_team_names(bs, info)
        self.add_goals(bs, info)
        self.add_stats(bs, info)
        self.add_result_infos(bs, info)
        self.add_game_info(bs, info)
        
        print(f"season {info.game_info_get('season')}")
        print(f"{info.game_info_get('date')} {info.game_info_get('time')} - {info.game_info_get('playday')}. Playday")
        print(f"{info.game_info_get('stadium')} in {info.game_info_get('location')} - {info.game_info_get('visitors')} visitors")
        print(f"referee {info.game_info_get('referee')}")
        print("Home")
        for key, value in info.home_team.items():
            print(f"{key}: {value}")
        
        print("Away")
        for key, value in info.away_team.items():
            print(f"{key}: {value}")
        
        return info
    
    def add_team_names(self, bs, info):
        names = bs.findAll("span", {"class": "verein-name"})
        home_name = names[0].get_text()
        away_name = names[2].get_text()
        info.home_team_add_info("name", home_name)
        info.away_team_add_info("name", away_name)
    
    def add_goals(self, bs, info):
        goals = bs.find("div", {"class": "box-spiel-ergebnis"})
        home_goals, away_goals = goals.get_text().split(":")
        info.home_team_add_info("goals", home_goals)
        info.away_team_add_info("goals", away_goals)
    
    def add_stats(self, bs, info):
        stats = bs.find("div", {"class": "box bs hide-empty"}).findAll("div", {"class": "col-md-6"})
        for stat in stats:
            for stat_child in stat.children:
                self._add_stat(info, stat_child)
    
    def _add_stat(self, info, stat):
        desc = stat.find("div", {"class": "text-center"})
        if desc:
            desc = desc.get_text()
            desc = desc_swapper(desc)
            home_stat, away_stat = stat.find_all("span")
            home_stat = check_cast_to_float(home_stat.get_text())
            away_stat = check_cast_to_float(away_stat.get_text())
            info.home_team_add_info(desc, home_stat)
            info.away_team_add_info(desc, away_stat)
    
    def add_result_infos(self, bs, info):
        result_infos = list(bs.find("div", {"class": "ergebnis-info"}).children)[1]
        self._add_season_time(info, result_infos)
        self._add_date_playday(info, result_infos)

    def _add_date_playday(self, info, result_infos):
        result_infos = result_infos.get_text()
        result_infos = result_infos[result_infos.find("-") + 1:]
        playday = result_infos[:result_infos.find(".")].strip()
        result_infos = result_infos[result_infos.find("-") + 1:]
        if "-" in result_infos:
            result_infos = result_infos[:result_infos.find("-")]
        date = result_infos[result_infos.find(",") + 1:].strip()
        info.game_info_add("date", date)
        info.game_info_add("playday", playday)

    def _add_season_time(self, info, result_infos):
        season_time = result_infos.findAll("span", {"class": "hidden-mini"})
        time = ""
        if is_time_included(season_time):
            season, time = season_time
            season = season.get_text()
            time = time.get_text().strip()
            time = time.replace("Uhr", "").strip()
        else:
            season = season_time[0].get_text()
        info.game_info_add("time", time)
        info.game_info_add("season", season)
    
    def add_game_info(self, bs, info):
        game_infos = bs.find("div", {"class": "box bs green-top box-spielinfos"})
        if game_infos:
            referee, location, stadium, visitors = [i.get_text() for i in
                                                    game_infos.findAll("b", {"class": "pull-right"})]
            info.game_info_add("referee", referee)
            info.game_info_add("location", location)
            info.game_info_add("stadium", stadium)
            info.game_info_add("visitors", visitors)
