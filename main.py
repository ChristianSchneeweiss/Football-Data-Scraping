import os
import time
from multiprocessing import Pool, Queue, cpu_count

from gamescraper import GameScraper
import pandas as pd


def get_urls():
    lines = []
    with open("test-urls.txt") as f:
        line = f.readline()
        while line:
            lines.append(line)
            line = f.readline()
    
    return lines


def scrape(url):
    scraper = GameScraper(url)
    info = scraper.scrape()
    print(f"Process id: {os.getpid()}")
    print(info.short_str())
    print("\n")
    return info


def spawn_scraping_processes(urls, processes=(cpu_count() - 1)):
    with Pool(processes=processes) as pool:
        infos = pool.map(scrape, urls)


def main():
    urls = get_urls()
    spawn_scraping_processes(urls)


if __name__ == '__main__':
    main()
