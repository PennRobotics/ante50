Ante50 Poker Tools
==================
> _sql branch_

## SQL

Since one goal of this project is to store statistical data about each element of a poker session&mdash;the game, table, player, hand, betting, et cetera&mdash;a relational database just makes sense, and CS50 devotes three hours of instruction to the subject, including a hearty introduction to SQL.

There are additional benefits to using SQL:

- data can be retrieved outside of the Python script (including external visualization!)
- data could be stored persistently (each session adds to the database rather than replaces it)
- potential space savings
- faster data access
- possibly simple syntax compared to creating inter-class relations in Python


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

**sql**
: replacing class-held statistical data with an external SQL database file

## Contributing

Feel free to create Issues or Pull Requests, or to fork this and make it awesome, or to make your own competing software

