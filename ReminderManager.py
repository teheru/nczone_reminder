import gi
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk

import threading
import time

from ReminderUI import ReminderUI
from ReminderConfig import ReminderConfig
from ReminderAPI import ReminderAPI
from ReminderNotify import ReminderNotify

class ReminderManager:
    def __init__(self):
        self._config = ReminderConfig()
        self._config.read()
        self._ui = ReminderUI()
        self._ui.apply_config(self._config.as_dict())
        self._api = ReminderAPI(self._config.api)
        self._notify = ReminderNotify()

        self._loop = ReminderManager.ReminderLoop(self._remind, self._config.pause, self._config.interval)

        self._ui.register_quit_callback(self._config.write)
        self._ui.register_quit_callback(self._loop.quit)
        self._ui.register_change_callback(self._ui_change)

        self._api.register_login_callback(self._login)
        self._api.register_logout_callback(self._logout)
        self._api.register_draw_callback(self._draw)
        self._api.register_error_callback(self._error)

        self._loop.start()

        Gtk.main()
    
    class ReminderLoop(threading.Thread):
        def __init__(self, fct, pause, interval):
            threading.Thread.__init__(self)

            self._fct = fct
            self.change_pause(pause)
            self.change_interval(interval)
            self.alive = True
        
        def run(self):
            since = 240
            while(self.alive):
                if not self._pause:
                    if since >= self._interval:
                        self._fct()
                        since = 0
                    else:
                        since += 1
                time.sleep(1)
        
        def change_pause(self, pause):
            self._pause = pause
        
        def change_interval(self, interval):
            self._interval = interval
        
        def quit(self):
            self.alive = False

    def _remind(self):
        self._api.query_logged_in()
        self._api.query_matches(self._config.username)


    def _ui_change(self, username, api, interval, loginout, draw, sound, notification, pause):
        self._config.update({
            'username': username,
            'api': api,
            'interval': interval,
            'loginout': loginout,
            'draw': draw,
            'sound': sound,
            'notification': notification,
            'pause': pause
        })
        self._api.update(api)
        self._api.reset_in_match()
        self._loop.change_pause(pause)
        self._loop.change_interval(interval)
    
    def _login(self):
        if self._config.loginout:
            if self._config.sound:
                self._notify.sound('login')
            if self._config.notification:
                self._notify.message('login')
    
    def _logout(self):
        if self._config.loginout:
            if self._config.sound:
                self._notify.sound('logout')
            if self._config.notification:
                self._notify.message('logout')

    def _draw(self):
        if self._config.draw:
            if self._config.sound:
                self._notify.sound('draw')
            if self._config.notification:
                self._notify.message('draw')
    
    def _error(self):
        if self._config.sound:
            self._notify.sound('error')
        if self._config.notification:
            self._notify.message('error')

if __name__ == '__main__':
    ReminderManager()