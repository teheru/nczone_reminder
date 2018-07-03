import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
import pygame
import time

class ReminderNotify:
    __login = 'login.ogg'
    __logout = 'logout.ogg'
    __draw = 'match.ogg'
    __error = 'error.ogg'

    def __init__(self):
        Notify.init('nC Zone Reminder')
        pygame.init()
    
    def sound(self, kind):
        if(kind == 'login'):
            self._sound(self.__login)
        elif(kind == 'logout'):
            self._sound(self.__logout)
        elif(kind == 'draw'):
            self._sound(self.__draw)
        elif(kind == 'error'):
            self._sound(self.__error)
    
    def message(self, kind):
        if(kind == 'login'):
            self._message('Jemand hat sich eingeloggt!')
        elif(kind == 'logout'):
            self._message('Jemand hat sich ausgeloggt.')
        elif(kind == 'draw'):
            self._message('Du wurdest gelost')
        elif(kind == 'error'):
            self._message('Es ist ein Fehler aufgetreten!')
    
    def _message(self, message):
        Notify.Notification.new('nC Zone Reminder', message).show()

    def _sound(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
