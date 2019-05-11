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


class GameScraper:
    def __init__(self, url):
        self.url = url
    
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
    
    def add_game_info(self, bs, info):
        game_infos = bs.find("div", {"class": "box bs green-top box-spielinfos"})
        if game_infos:
            referee, location, stadium, visitors = [i.get_text() for i in
                                                    game_infos.findAll("b", {"class": "pull-right"})]
            info.game_info_add("referee", referee)
            info.game_info_add("location", location)
            info.game_info_add("stadium", stadium)
            info.game_info_add("visitors", visitors)
    
    def add_result_infos(self, bs, info):
        result_infos = list(bs.find("div", {"class": "ergebnis-info"}).children)[1]
        season_time = result_infos.findAll("span", {"class": "hidden-mini"})
        season = ""
        time = ""
        if len(season_time) >= 2:
            season, time = season_time
            season = season.get_text()
            time = time.get_text().strip()
            time = time.replace("Uhr", "").strip()
        elif len(season_time) == 1:
            season = season_time[0].get_text()
        result_infos = result_infos.get_text()
        result_infos = result_infos[result_infos.find("-") + 1:]
        playday = result_infos[:result_infos.find(".")].strip()
        result_infos = result_infos[result_infos.find("-") + 1:]
        if "-" in result_infos:
            result_infos = result_infos[:result_infos.find("-")]
        date = result_infos[result_infos.find(",") + 1:].strip()
        print(time)
        info.game_info_add("time", time)
        info.game_info_add("date", date)
        info.game_info_add("season", season)
        info.game_info_add("playday", playday)
    
    def add_stats(self, bs, info):
        stats = bs.find("div", {"class": "box bs hide-empty"}).findAll("div", {"class": "col-md-6"})
        for stat in stats:
            for c in stat.children:
                desc = c.find("div", {"class": "text-center"})
                if desc:
                    desc = desc.get_text()
                    desc = desc_swapper(desc)
                    home_stat, away_stat = c.find_all("span")
                    home_stat = home_stat.get_text().replace(",", ".")
                    away_stat = away_stat.get_text().replace(",", ".")
                    info.home_team_add_info(desc, home_stat)
                    info.away_team_add_info(desc, away_stat)
    
    def add_team_names(self, bs, info):
        names = bs.findAll("span", {"class": "verein-name"})
        home_name = names[0].get_text()
        away_name = names[2].get_text()
        info.home_team = {"name": home_name}
        info.away_team = {"name": away_name}
    
    def _get_html(self):
        html = urlopen(self.url)
        bs = BeautifulSoup(html.read(), "html.parser")
        return bs
    
    def add_goals(self, bs, info):
        goals = bs.find("div", {"class": "box-spiel-ergebnis"})
        homegoals, awaygoals = goals.get_text().split(":")
        info.home_team_add_info("goals", homegoals)
        info.away_team_add_info("goals", awaygoals)
