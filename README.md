ante50
======
> _gui branch_

## GUI

To improve the portability and reach of this project, I'm considering a variety of user interfaces. In increasing order of complexity:

- console
- file I/O
- curses
- SDL2
- Pygame
- tkinter
- GTK via PyGObject
- something browser-based

These probably would make use of such libraries as [Pillow](https://python-pillow.org/).

### Graphics Resources

For _curses_ (or _ncurses_ or _notcurses_), cards, chips, and table would be custom-built with colors and special character poker symbols or emojis

For graphical options, I hope to generate vector graphics rather than use the primitives available in each library unless absolutely necessary.

### Development Strategy

Ideally, game logic would be removed from each function and the functions would be used only to generate example data transfer between the GUI and the rest of the ante50 engine. This branch should _purely_ focus on getting each GUI method perfected and enforcing something like a model-view-controller pattern, where ALL view-related functionality is in its own class, which has no program logic whatsoever.

Currently, <tt>[pviz.py](pviz.py)</tt> has the GUI selection and necessary imports for eventual transfer into <tt>[ante50.py](ante50.py)</tt>.

## Branches

**main**
: will probably be largely untouched until one of the branches shows great promise

**cs50**
: trimming down the (overly-ambitious) current version so that everything works properly and has code coverage

**develop**
: writing more tests and engine functionality

**gui**
: experimenting with threads and info exchange via a GUI

**meson**
: trying to set up a build system (inspired by the GNOME Drawing app, which I was surprised to discover is written in Python)

**optim**
: profiling, code coverage, finding decorators and data structures and execution strategies to open up performance

**montecarlo**
: removing user input so strategy definitions can be tested against one another

## Contributing

Feel free to create Issues or Pull Requests, or to fork this and make it awesome, or to make your own competing software

