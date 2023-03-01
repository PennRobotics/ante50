# No idea if this will work, but here we go! (TODO)

from enum import Enum, auto

class Gui(Enum):
    STDIO = auto()
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
                print('f')
            case Gui.CONSOLE:
                print('c')
            case Gui.CURSES:
                print('n')
            case Gui.SDL2:
                print('s')
            case Gui.TKINTER:
                print('t')
            case Gui.PYGAME:
                print('p')
            case _:
                raise ValueError('unexpected case')
        # TODO: timed thread for display, thread for data
        # TODO: pass from one thread to other
        # TODO: how to wait for input in each method?
        g.run()


if __name__=='__main__':
    g = G()  # TODO-debug
    frontend = Frontend(Gui.STDIO, g)
