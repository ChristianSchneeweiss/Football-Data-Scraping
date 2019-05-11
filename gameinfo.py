class GameInfo:
    def __init__(self):
        self._info = {"home team": {}, "away team": {}, "game info": {}}
    
    @property
    def info(self):
        d = {}
        for key in self._info.keys():
            for k, v in self._info[key].items():
                if key == "game info":
                    d[k] = v
                else:
                    d[f"{key} {k}"] = v
        return d
    
    @property
    def home_team(self):
        return self._info["home team"]
    
    @home_team.setter
    def home_team(self, value):
        self._info["home team"] = value
    
    def home_team_add_info(self, desc, value):
        self._info["home team"][desc] = value
    
    def home_team_get(self, desc):
        if desc in self._info["home team"]:
            return self._info["home team"][desc]
        return None
    
    @property
    def away_team(self):
        return self._info["away team"]
    
    @away_team.setter
    def away_team(self, value):
        self._info["away team"] = value
    
    def away_team_add_info(self, desc, value):
        self._info["away team"][desc] = value
    
    def away_team_get(self, desc):
        if desc in self._info["away team"]:
            return self._info["away team"][desc]
        return None
    
    def game_info_add(self, desc, value):
        self._info["game info"][desc] = value
    
    def game_info_get(self, desc):
        if desc in self._info["game info"]:
            return self._info["game info"][desc]
        return None
    
    def __str__(self):
        s = f"season {self.game_info_get('season')}\n"
        s += f"{self.game_info_get('date')} {self.game_info_get('time')} - {self.game_info_get('gameday')}. gameday\n"
        s += f"{self.game_info_get('stadium')} in {self.game_info_get('location')} - {self.game_info_get('visitors')} visitors\n"
        s += f"referee {self.game_info_get('referee')}\n\n"
        
        s += f"Home Team: {self.home_team_get('name')}\n"
        for key, value in self.home_team.items():
            s += f"{key}: {value}\n"
        s += "\n"
        
        s += f"Away Team: {self.away_team_get('name')}\n"
        for key, value in self.away_team.items():
            s += f"{key}: {value}\n"
        
        return s
    
    def short_str(self):
        return f"{self.game_info_get('season')} {self.game_info_get('league')} {self.game_info_get('gameday')}.day: {self.home_team_get('name')}" + \
               f" {self.home_team_get('goals')} :" + \
               f" {self.away_team_get('goals')} {self.away_team_get('name')}"
