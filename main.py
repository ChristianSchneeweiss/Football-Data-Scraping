import os
from multiprocessing import Pool, cpu_count

from gamescraper import GameScraper


def get_urls():
    lines = []
    with open("test-urls.txt") as f:
        line = f.readline()
        while line:
            lines.append(line)
            line = f.readline()
    
    return lines


def scrape_game(url):
    scraper = GameScraper(url)
    info = scraper.scrape()
    print(f"Process id: {os.getpid()}")
    print(info.short_str())
    print("\n")
    return info


def spawn_game_scraping_processes(urls, processes=(cpu_count() - 1 or 1)):
    with Pool(processes=processes) as pool:
        infos = pool.map(scrape_game, urls)
    return infos


def main():
    urls = get_urls()
    # print(scrape_game(urls[2]))
    infos = spawn_game_scraping_processes(urls)
    for info in infos:
        print(info)


if __name__ == '__main__':
    main()
