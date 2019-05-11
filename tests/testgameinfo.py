import unittest
from gameinfo import GameInfo


class MyTestCase(unittest.TestCase):
    def test_home_team(self):
        info = GameInfo()
        info.home_team_add_info("test 1", "15")
        info.home_team_add_info("test 2", "2315")
        info.home_team_add_info("test 3", 12)
        info.home_team_add_info("test 4", "Hello World")
        self.assertEqual(info.home_team_get("test 1"), "15")
        self.assertEqual(info.home_team_get("test 2"), "2315")
        self.assertEqual(info.home_team_get("test 3"), 12)
        self.assertEqual(info.home_team_get("test 4"), "Hello World")
        self.assertIsNone(info.home_team_get("test 5"))
        
        d = {"test 1": "15", "test 2": "2315", "test 3": 12, "test 4": "Hello World"}
        self.assertDictEqual(info.home_team, d)
    
    def test_away_team(self):
        info = GameInfo()
        info.away_team_add_info("test 1", "15")
        info.away_team_add_info("test 2", "2315")
        info.away_team_add_info("test 3", 12)
        info.away_team_add_info("test 4", "Hello World")
        self.assertEqual(info.away_team_get("test 1"), "15")
        self.assertEqual(info.away_team_get("test 2"), "2315")
        self.assertEqual(info.away_team_get("test 3"), 12)
        self.assertEqual(info.away_team_get("test 4"), "Hello World")
        self.assertIsNone(info.away_team_get("test 5"))

        d = {"test 1": "15", "test 2": "2315", "test 3": 12, "test 4": "Hello World"}
        self.assertDictEqual(info.away_team, d)
    
    def test_game_info(self):
        info = GameInfo()
        info.game_info_add("test 1", "15")
        info.game_info_add("test 2", "2315")
        info.game_info_add("test 3", 12)
        info.game_info_add("test 4", "Hello World")
        self.assertEqual(info.game_info_get("test 1"), "15")
        self.assertEqual(info.game_info_get("test 2"), "2315")
        self.assertEqual(info.game_info_get("test 3"), 12)
        self.assertEqual(info.game_info_get("test 4"), "Hello World")
        self.assertIsNone(info.game_info_get("test 5"))
        
    def test_info(self):
        info = GameInfo()
        info.game_info_add("test 1", "15")
        info.away_team_add_info("test 2", "23")
        info.home_team_add_info("test 3", "2")
        info.game_info_add("test 4", "567")
        info.away_team_add_info("test 5", "345")
        info.home_team_add_info("test 6", "12")
        
        d = {"test 1": "15", "test 4": "567", "away test 2": "23", "away test 5": "345", "home test 3": "2", "home test 6": "12"}
        self.assertDictEqual(info.info, d)


if __name__ == '__main__':
    unittest.main()
