from bs4 import BeautifulSoup
import requests


def scrape(year: int = 2015, nation: str = "spanien") -> [str]:
    soup = _get_soup(nation, year)
    gameday_blocks = _get_gameday_blocks(soup)
    game_links = []
    for gameday_block in gameday_blocks:
        games = _get_games_in_gameday_block(gameday_block)
        game_links += (_get_game_links_from_games(games))
    
    return _create_full_url(game_links)


def _get_soup(nation, year):
    url = f"https://www.fussballdaten.de/{nation}/{year}/spielplan/"
    html = requests.get(url)
    bs = BeautifulSoup(html.text, "html.parser")
    return bs


def _get_gameday_blocks(soup):
    return soup.find_all("div", {"class": "col-md-4"})


def _get_games_in_gameday_block(gameday_block):
    return gameday_block.find_all("td", {"data-col-seq": "4"})


def _get_game_links_from_games(games):
    game_links = []
    for game in games:
        game_link = game.find("a")
        if _game_is_played(game_link) and _is_a_game_link(game_link):
            game_links.append(game_link.get("href"))
    
    return game_links


def _game_is_played(game_link):
    return len(game_link.get_text()) < 4


def _is_a_game_link(game_link):
    return not "vereine" in game_link.get("href")


def _create_full_url(game_links):
    return list(map(lambda link: "https://www.fussballdaten.de" + link, game_links))
