import urllib.request
import json

class ReminderAPI:
    def __init__(self, api):
        self._login_callback = []
        self._logout_callback = []
        self._draw_callback = []
        self._error_callback = []

        self._logged_in_ids = set()
        self._in_match = []

        self.update(api)
    
    def update(self, api):
        self._api = api
        self._api_logged_in = self._api + '/players/logged_in'
        self._api_matches = self._api + '/matches/running'
    
    def query_logged_in(self):
        try:
            data = json.loads(urllib.request.urlopen(self._api_logged_in).read())
        except:
            for fct in self._error_callback:
                fct()
            data = []

        temp_ids = set()
        for player in data:
            temp_ids.add(player['id'])
        
        login_players = temp_ids - self._logged_in_ids
        logout_players = self._logged_in_ids - temp_ids
        self._logged_in_ids = temp_ids

        if len(login_players) > 0:
            for fct in self._login_callback:
                fct()
            
        if len(logout_players) > 0:
            for fct in self._logout_callback:
                fct()
    
    def query_matches(self, username):
        lusername = username.lower()

        try:
            data = json.loads(urllib.request.urlopen(self._api_matches).read())
        except:
            for fct in self._error_callback:
                fct()
            data = []

        temp_in_match = False
        for match in data:
            players = match['players']['team1'] + match['players']['team2']
            for player in players:
                if player['username'].lower() == lusername:
                    temp_in_match = True
                    break
            if temp_in_match: break
        
        drawed = temp_in_match and not self._in_match
        self._in_match = temp_in_match

        if drawed:
            for fct in self._draw_callback:
                fct()
    
    def reset_in_match(self):
        self._in_match = False
    
    def register_login_callback(self, fct):
        self._login_callback.append(fct)
    
    def register_logout_callback(self, fct):
        self._logout_callback.append(fct)
    
    def register_draw_callback(self, fct):
        self._draw_callback.append(fct)
    
    def register_error_callback(self, fct):
        self._error_callback.append(fct)
