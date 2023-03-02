## Development Plan

I am currently contemplating moving to Meson and splitting the functionality of this program across fairly clear lines. I also want to take part in the CS50P final project (which is where the 50 suffix originates), and much of the ability to move fast comes from writing Python code instead of figuring out build systems, dependencies, GUI frameworks, and so on. Thus, I am creating a series of project milestones as well as multiple branches:

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

## Classes

| Stats |
| ----- |
| _Keeps a record of actions and reactions_ |
| `calculate_ev()` (TODO) distill stats to a signed float showing lifetime per-hand expected value |

| Strategy |   |
| -------- | - |
| _Determines action based on available information with optional random variation_ |  |
| `get_preflop_action(hole_str, seat_pos)` (TODO) returns the Action recommended for a pair of hole cards using parameters in Strategy | `hole_str` examples: `"AKs"`, `"JJ"`, `"T4"` |


| Player |
| ------ |
| _Contains member variables for a player: name, chips, involvement in game, position, personal stats and strategy, etc. |


| OtherHolePredictor |
| ------------------ |
| _List guess of opponent hole cards using available information_ (TODO) |


| DrawFinder |  |
| ---------- | - |
| _Figure out specific draws available based on visible cards_ |  |
| `get_draws(hole_set, board_set)` (TODO) | set example: `set(['Kh', '4d'])` |


| Hand |
| ---- |
| _Provides value of a hand_  
  `(hand_set, owner=None)` |
| `owner` determines who the hand belongs, for use during showdown |
| `get_value(hand_set, owner=None)` |  <!-- TODO -->
| `__str__()` |  <!-- TODO -->
| `__repr__()` |  <!-- TODO -->
| `compare(other)` -- returns -1, 0, or 1 to indicate loss, tie, or win |
| `number_of_outs()` (TODO) |


| Game |
| ---- |
| _Creates a group of players and table/game statistics_ |
| `remove_player(idx)` (TODO) |
| `play()` -- begin the main state machine to get player input and display table and players |
| `begin_round()` -- advance button, shuffle deck and reset interator, reset per-hand variables |
| `show_table_and_get_action()` -- a wrapper to call `show_table()` and `get_action()` |
| `show_table()` -- stdio display of table, uses a cursor movement escape sequence to update display |
| `get_action()` -- gets player input and decides action of non-controlled opponents |
| `advance_round()` -- draws cards and sets bet amount for the current round |
| `decide_winner()` -- compares each player in an array, eliminating losing hands |


### Top-level Functions

`reshuffle()` -- resets `known` and `unknown` card sets, applies `random.shuffle` to `deck`, creates an iterator for providing the next card

`draw_card()` -- takes a card from the playing deck iterator (`from_deck`) and updates `known` and `unknown` cards if visible

`card_name()` -- provides a plaintext description of a single card

## Improvement

### Unit testing

To run the [pytest](https://github.com/pytest-dev/pytest/) test suite: `pip install pytest` followed by `pytest test_ante50.py`

### Code coverage

Coverage can be easily recorded via `pip install coverage`, then `coverage run ante50.py` and eventually `coverage html` or `coverage report`

