from gamescraper import GameScraper
from gamescraper import check_cast_to_float


def get_urls():
    lines = []
    with open("test-urls.txt") as f:
        line = f.readline()
        while line:
            lines.append(line)
            line = f.readline()
    
    return lines


def main():
    for url in get_urls():
        # scraper = GameScraper(get_urls()[0])
        scraper = GameScraper(url)
        scraper.scrape()


if __name__ == '__main__':
    main()
