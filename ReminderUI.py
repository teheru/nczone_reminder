import gi
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk

class ReminderUI:
    def __init__(self):
        self._change_callback = []
        self._quit_callback = []

        builder = Gtk.Builder()
        builder.add_from_file('reminder.ui')
        builder.connect_signals(self)

        self._window = builder.get_object('main_window')

        self._username = builder.get_object("username_entry")
        self._api = builder.get_object("api_entry")
        self._interval = builder.get_object("interval")
        self._loginout = builder.get_object("loginout_toggle")
        self._draw = builder.get_object("draw_toggle")
        self._sound = builder.get_object("sound_toggle")
        self._notification = builder.get_object("notification_toggle")
        self._pause = builder.get_object("pause_toggle")

        self._window.connect('destroy', self._quit)

        self._window.show_all()
    
    def apply_config(self, config):
        self._username.set_text(config['username'])
        self._api.set_text(config['api'])
        self._interval.set_value(config['interval'])
        self._loginout.set_active(config['loginout'])
        self._draw.set_active(config['draw'])
        self._sound.set_active(config['sound'])
        self._notification.set_active(config['notification'])
        self._pause.set_active(config['pause'])
    
    def _on_change(self, source):
        for fct in self._change_callback:
            fct(
                self._username.get_text(),
                self._api.get_text(),
                int(self._interval.get_value()),
                self._loginout.get_active(),
                self._draw.get_active(),
                self._sound.get_active(),
                self._notification.get_active(),
                self._pause.get_active()
            )

    def _quit(self, source):
        for fct in self._quit_callback:
            fct()
        exit(0)
    
    def register_change_callback(self, fct):
        self._change_callback.append(fct)

    def register_quit_callback(self, fct):
        self._quit_callback.append(fct)
