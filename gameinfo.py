class GameInfo:
    def __init__(self):
        self._info = {"home team": {}, "away team": {}, "game info": {}}
    
    @property
    def home_team(self):
        return self._info["home team"]
    
    @home_team.setter
    def home_team(self, value):
        self._info["home team"] = value
    
    def home_team_add_info(self, desc, value):
        self._info["home team"][desc] = value
    
    @property
    def away_team(self):
        return self._info["away team"]
    
    @away_team.setter
    def away_team(self, value):
        self._info["away team"] = value
    
    def away_team_add_info(self, desc, value):
        self._info["away team"][desc] = value
    
    def game_info_add(self, desc, value):
        self._info["game info"][desc] = value
    
    def game_info_get(self, desc):
        if desc in self._info["game info"]:
            return self._info["game info"][desc]
        return None
