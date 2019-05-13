import os
from multiprocessing import Pool, cpu_count
from time import time

import pandas as pd

from gamescraper import GameScraper
import urlscraper


def get_test_urls():
    lines = []
    with open("test-urls.txt") as f:
        line = f.readline()
        while line:
            lines.append(line)
            line = f.readline()
    
    return lines


def get_urls(years=None, nations=None):
    if nations is None:
        nations = ["spanien"]
    if years is None:
        years = [2019]
    urls = []
    for nation in nations:
        for year in years:
            urls += urlscraper.scrape(year, nation)
    return urls


def scrape_game(url):
    scraper = GameScraper(url)
    start = time()
    info = scraper.scrape()
    end = time()
    print(f"Took {(end - start) * 1000} milliseconds")
    print(f"Process id: {os.getpid()}")
    print(info.short_str())
    print("\n")
    return info


def spawn_game_scraping_processes(urls, processes=(cpu_count() - 1 or 4)):
    with Pool(processes=processes) as pool:
        infos = pool.map(scrape_game, urls)
    return infos


def main():
    years = list(range(2011, 2019))
    nations = ["spanien", "england", "bundesliga", "italien", "frankreich"]
    for year in years:
        for nation in nations:
            urls = get_urls([year], [nation])
            # urls = get_test_urls()
            print(f"scraping {len(urls)} urls")
            print(f"starting with {nation} {year}")
            i = []
            infos = spawn_game_scraping_processes(urls)
            for info in infos:
                print(info)
                i.append(info.info)
            
            df = pd.DataFrame(i)
            df.to_csv(f"data/{nation}{year}.csv", index=False)
            print(f"wrote {nation}{year} dataset")


if __name__ == '__main__':
    main()
