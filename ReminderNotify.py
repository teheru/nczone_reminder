import os
MSWINDOWS = os.name == 'nt'

from plyer import notification
if MSWINDOWS:
    import winsound
else:
    import pygame
import time

class ReminderNotify:
    if MSWINDOWS:
        __login = 'login.wav'
        __logout = 'logout.wav'
        __draw = 'match.wav'
        __error = 'error.wav'
    else:
        __login = 'login.ogg'
        __logout = 'logout.ogg'
        __draw = 'match.ogg'
        __error = 'error.ogg'

    def __init__(self):
        if not MSWINDOWS:
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
        notification.notify(title='nC Zone Reminder', message=message, app_name="nC Zone Reminder")

    def _sound(self, filename):
        if MSWINDOWS:
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        else:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
