# No idea if this will work, but here we go! (TODO)

from enum import Enum, auto
import threading

class Gui(Enum):
    FILEIO = auto()
    CONSOLE = auto()
    CURSES = auto()
    SDL = auto()
    TKINTER = auto()
    PYGAME = auto()

class G:  # TODO-debug
    def __init__(self):
        self.id = 1

    def run(self):
        print('run')


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
            case Gui.TKINTER:
                import tkinter
            case Gui.PYGAME:
                import pygame
            case _:
                raise ValueError('unexpected case')
        self.mode = mode
        # TODO: timed thread for display, thread for data
        # TODO: pass from one thread to other
        # TODO: how to wait for input in each method?
        self.disp_thread = threading.Thread(target=self.disp)
        self.g_thread = threading.Thread(target=gh.run)
        self.g_thread.start()
        self.disp_thread.start()
        while True:
            pass  # TODO-debug

    def disp(self):
        match self.mode:
            case Gui.FILEIO:
                print('disp f')
            case Gui.CONSOLE:
                print('disp c')
            case Gui.CURSES:
                print('disp n')
            case Gui.SDL2:
                print('disp s')
            case Gui.TKINTER:
                print('disp t')
            case Gui.PYGAME:
                print('disp p')
            case _:
                raise ValueError('unexpected case')


if __name__=='__main__':
    g = G()  # TODO-debug
    frontend = Frontend(Gui.CONSOLE, g)
