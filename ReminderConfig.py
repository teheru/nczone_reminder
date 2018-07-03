import json

class ReminderConfig:
    __filename = 'config'

    def __init__(self):
        self.username = ''
        self.api = ''
        self.interval = 30
        self.loginout = True
        self.draw = True
        self.sound = True
        self.notification = True
        self.pause = True
    
    def read(self):
        try:
            with open(self.__filename) as fp:
                self.update(json.load(fp))
        except FileNotFoundError:
            print("No config file found, skipping")
    
    def write(self):
        d = self.as_dict()
        with open(self.__filename, 'w') as fp:
            json.dump(d, fp)
    
    def update(self, config):
        self.username = config['username']
        self.api = config['api']
        self.interval = config['interval']
        self.loginout = config['loginout'] == 1
        self.draw = config['draw'] == 1
        self.sound = config['sound'] == 1
        self.notification = config['notification'] == 1
        self.pause = config['pause'] == 1

        if self.interval < 5 or self.interval > 240:
            self.interval = 30

    def as_dict(self):
        return {
            'username': self.username,
            'api': self.api,
            'interval': self.interval,
            'loginout': self.loginout,
            'draw': self.draw,
            'sound': self.sound,
            'notification': self.notification,
            'pause': self.pause,
        }