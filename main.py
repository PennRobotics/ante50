import sys
import gi

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, GObject, Gio

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='ante50.app',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MyWindow('Gtk4 POC', 400, 500, application=self)
        win.present()


def main():
    ante50_gtk = Application()
    return ante50_gtk.run(sys.argv)

