from urllib.request import urlopen

from bs4 import BeautifulSoup

from gameinfo import GameInfo


def _desc_swapper(desc):
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
        return "blocked by goalkeeper"
    elif "Fouls" in desc:
        return "fouls"
    elif "Zweikämpfe" in desc:
        return "tackles won %"
    elif "Pässe" in desc:
        return "passes quote %"
    elif "Gelbe Karten" in desc:
        return "yellow cards"
    elif "Platzverweise" in desc:
        return "red cards"
    return desc


def _check_cast_to_float(stat):
    stat = stat.replace(",", ".")
    try:
        stat = float(stat)
        return stat
    except ValueError as e:
        return stat


def _is_time_included(season_time):
    return len(season_time) >= 2


def _clean_name(name):
    name = name.get_text()
    if "(" in name:
        name = name[:name.find("(")]
    return name


def _get_link(a):
    return a.get("href")


def _get_name(player_link):
    html = urlopen("https://www.fussballdaten.de" + player_link)
    bs = BeautifulSoup(html.read(), "html.parser")
    name = bs.h1.get_text()
    return name


class GameScraper:
    def __init__(self, url):
        self.url = url
        self._bs = None
        self._info = GameInfo()
    
    def _get_html(self, path=""):
        html = urlopen(self.url.strip() + path)
        bs = BeautifulSoup(html.read(), "html.parser")
        return bs
    
    def scrape(self) -> GameInfo:
        self._scrape_detail_page()
        self._scrape_line_up_page()
        return self._info
    
    def _scrape_detail_page(self):
        self._bs = self._get_html()
        self._add_team_names()
        self._add_goals()
        self._add_stats()
        self._add_result_infos()
        self._add_game_info()
    
    def _scrape_line_up_page(self):
        self._bs = self._get_html("aufstellung")
        self._add_home_coach()
        self._add_away_coach()
        self._add_home_line_up()
        self._add_away_line_up()
    
    def _add_away_coach(self):
        try:
            away_coach = self._bs.find_all("div", {"class": "gast-content"})[2].find("a", {"class": "text lineup"}).get_text()
            self._info.away_team_add_info("coach", away_coach)
        except AttributeError:
            pass
    
    def _add_home_coach(self):
        try:
            home_coach = self._bs.find_all("div", {"class": "heim-content"})[2].find("a", {"class": "text lineup"}).get_text()
            self._info.home_team_add_info("coach", home_coach)
        except AttributeError:
            pass
    
    def _add_home_line_up(self):
        home = self._bs.find("div", {"class": "heim-content"})
        try:
            names = home.find("div", {"class": "box-taktik"}).findAll("a", {"class": "name"})
        except AttributeError:
            names = home.findAll("a", {"class": "text lineup"})
        player_links = list(map(_get_link, names))
        names = list(map(_get_name, player_links))
        self._info.home_team_add_info("lineup", names)
    
    def _add_away_line_up(self):
        away = self._bs.find("div", {"class": "gast-content"})
        try:
            names = away.find("div", {"class": "box-taktik"}).findAll("a", {"class": "name"})
        except AttributeError:
            names = away.findAll("a", {"class": "text lineup"})
        player_links = list(map(_get_link, names))
        names = list(map(_get_name, player_links))
        self._info.away_team_add_info("lineup", names)
    
    def _add_team_names(self):
        names = self._bs.findAll("span", {"class": "verein-name"})
        home_name = names[0].get_text()
        away_name = names[2].get_text()
        self._info.home_team_add_info("name", home_name)
        self._info.away_team_add_info("name", away_name)
    
    def _add_goals(self):
        goals = self._bs.find("div", {"class": "box-spiel-ergebnis"})
        home_goals, away_goals = goals.get_text().split(":")
        self._info.home_team_add_info("goals", home_goals)
        self._info.away_team_add_info("goals", away_goals)
    
    def _add_stats(self):
        stats = self._bs.find("div", {"class": "box bs hide-empty"}).findAll("div", {"class": "col-md-6"})
        for stat in stats:
            for stat_child in stat.children:
                self._add_stat(stat_child)
    
    def _add_stat(self, stat):
        desc = stat.find("div", {"class": "text-center"})
        if desc:
            desc = desc.get_text()
            desc = _desc_swapper(desc)
            stats = stat.find_all("span")
            if len(stats) == 2:
                home_stat, away_stat = stats
                home_stat = _check_cast_to_float(home_stat.get_text())
                away_stat = _check_cast_to_float(away_stat.get_text())
                self._info.home_team_add_info(desc, home_stat)
                self._info.away_team_add_info(desc, away_stat)
    
    def _add_result_infos(self):
        result_infos = list(self._bs.find("div", {"class": "ergebnis-info"}).children)[1]
        self._add_season_time(result_infos)
        self._add_date_playday(result_infos)
    
    def _add_date_playday(self, result_infos):
        result_infos = result_infos.get_text()
        league = result_infos[:result_infos.find("-")]
        league = league.split()[:-1]
        league = " ".join(league)
        result_infos = result_infos[result_infos.find("-") + 1:]
        gameday = result_infos[:result_infos.find(".")].strip()
        result_infos = result_infos[result_infos.find("-") + 1:]
        if "-" in result_infos:
            result_infos = result_infos[:result_infos.find("-")]
        date = result_infos[result_infos.find(",") + 1:].strip()
        self._info.game_info_add("league", league)
        self._info.game_info_add("date", date)
        self._info.game_info_add("gameday", gameday)
    
    def _add_season_time(self, result_infos):
        season_time = result_infos.findAll("span", {"class": "hidden-mini"})
        time = ""
        if _is_time_included(season_time):
            season, time = season_time
            season = season.get_text()
            time = time.get_text().strip()
            time = time.replace("Uhr", "").strip()
        else:
            season = season_time[0].get_text()
        self._info.game_info_add("time", time)
        self._info.game_info_add("season", season)
    
    def _add_game_info(self):
        game_infos = self._bs.find("div", {"class": "box bs green-top box-spielinfos"})
        if game_infos:
            referee, location, stadium, visitors = [i.get_text() for i in
                                                    game_infos.findAll("b", {"class": "pull-right"})]
            self._info.game_info_add("referee", referee)
            self._info.game_info_add("location", location)
            self._info.game_info_add("stadium", stadium)
            self._info.game_info_add("visitors", visitors)
