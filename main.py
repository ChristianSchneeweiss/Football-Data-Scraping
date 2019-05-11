from gamescraper import GameScraper


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
        scraper = GameScraper(url)
        info = scraper.scrape()
        print(info)


if __name__ == '__main__':
    main()
