import unittest
from gamescraper import GameScraper


class MyTestCase(unittest.TestCase):
    def test_scraping(self):
        url = "https://www.fussballdaten.de/spanien/2019/34/huesca-eibar/"
        scraper = GameScraper(url)
        info = scraper.scrape()
        self.assertEqual(info.game_info_get("referee"), "David Medie Jimenez")
        self.assertEqual(info.game_info_get("location"), "Huesca")
        self.assertEqual(info.game_info_get("stadium"), "El Alcoraz")
        self.assertEqual(info.game_info_get("visitors"), "6157")
        self.assertEqual(info.home_team_get("name"), "SD Huesca")
        self.assertEqual(info.away_team_get("name"), "SD Eibar")
        self.assertEqual(info.home_team_get("goals"), 2)
        self.assertEqual(info.away_team_get("goals"), 0)
        self.assertIn("Marko Dmitrovic", info.away_team_get("lineup"))
        self.assertIn("Jorge Miramon", info.home_team_get("lineup"))
        


if __name__ == '__main__':
    unittest.main()
