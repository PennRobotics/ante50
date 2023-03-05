# No idea if this will work, but here we go! (TODO)

from ante50 import Game
from enum import Enum, auto
import threading

class Gui(Enum):
    FILEIO = auto()
    CONSOLE = auto()
    CURSES = auto()
    SDL2 = auto()
    TKINTER = auto()
    PYGAME = auto()
    GTK = auto()  # TODO
    FLASK = auto()  # TODO

class G:  # TODO-debug
    def __init__(self):
        self.id = 1

    def run(self):
        print('run')

# Uses PyGObject
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Frontend:
    def __init__(self, mode, gh):
        match mode:
            case Gui.FILEIO:
                print('(file i/o)')
            case Gui.CONSOLE:
                print('(console)')
            case Gui.CURSES:
                import platform
                match platform.system():
                    case 'Windows':
                        try:
                            import curses
                        except:
                            raise ImportError('pip install windows-curses')
                    case _:
                        import curses
            case Gui.SDL2:
                import sdl2.ext
            case Gui.TKINTER:  # TODO: or wxPython
                import tkinter
            case Gui.PYGAME:  # TODO: or Kivy
                import pygame
            case Gui.GTK:
                pass
            case Gui.FLASK:
                pass  # TODO
            case _:
                raise ValueError('unexpected case')
        self.mode = mode
        # TODO: timed thread for display, thread for data
        # TODO: pass from one thread to other
        # TODO: how to wait for input in each method?
        #self.disp_thread = threading.Thread(target=self.disp)
        #self.g_thread = threading.Thread(target=gh)
        #self.g_thread.start()
        #self.disp_thread.start()
        self.disp()
        ### while True:
        ###     pass  # TODO-debug

    def disp(self):
        match self.mode:
            case Gui.FILEIO:
                print('disp f')
                raise RuntimeError('TODO: implement')
            case Gui.CONSOLE:
                print('disp c')
                raise RuntimeError('TODO: implement')
            case Gui.CURSES:
                print('disp n')
                raise RuntimeError('TODO: implement')
            case Gui.SDL2:
                print('disp s')
                raise RuntimeError('TODO: implement')
            case Gui.TKINTER:
                print('disp t')
                raise RuntimeError('TODO: implement')
            case Gui.PYGAME:
                print('disp p')
                raise RuntimeError('TODO: implement')
            case Gui.GTK:
                window = Gtk.Window(title='test')
                window.show()
                window.connect('destroy', Gtk.main_quit)
                Gtk.main()
            case _:
                raise ValueError('unexpected case')


if __name__=='__main__':
    game = Game()  # TODO-debug
    frontend = Frontend(Gui.GTK, game.play_gui)
