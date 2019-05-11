from bs4 import BeautifulSoup
from urllib.request import urlopen


def scrape(year: int = 2015, nation: str = "spanien") -> [str]:
    url = f"https://www.fussballdaten.de/{nation}/{year}/spielplan/"
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), "html.parser")
    gamedays = bs.find_all("div", {"class": "col-md-4"})
    game_links = []
    for gameday in gamedays:
        games = gameday.find_all("td", {"data-col-seq": "4"})
        for game in games:
            game_link = game.find("a")
            if len(game_link.get_text()) < 4:
                if not "vereine" in game_link.get("href"):
                    game_links.append(game_link.get("href"))
    
    return list(map(lambda link: "https://www.fussballdaten.de" + link, game_links))
