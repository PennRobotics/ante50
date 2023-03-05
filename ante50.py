# TODO
# ====
# Display table
# Display players (name and relevant stats)
# Display cards
# Display cards as hand
# Display cards as board and discards
# Display chips (player stack, bets, pot, side pots) and dealer button
# Create action buttons
# Preferences pane (which info to show/hide, color scheme, etc.)
# Close up existing TODO tags
# Animation


# Imports
from collections import Counter
from enum import IntEnum, auto
from itertools import pairwise
from random import shuffle


# Consts
MAX_VER = 1
LIMIT_BET = 2
CURSOR_UP = '\033[1A' if True else ''
SUITS = 'cdhs'
VALUES = '23456789TJQKA'
WHEEL = 'A2345'

SUIT_NAME = { 'c': 'club',
              'd': 'diamond',
              'h': 'heart',
              's': 'spade' }

VALUE_NAME = { '2': 'deuce',
               '3': 'trey',
               '4': 'four',
               '5': 'five',
               '6': 'six',
               '7': 'seven',
               '8': 'eight',
               '9': 'nine',
               'T': 'ten',
               'J': 'jack',
               'Q': 'queen',
               'K': 'king',
               'A': 'ace' }

ROUND_NAME = { 0: 'Pre-flop',
               1: 'Flop',
               2: 'Turn',
               3: 'River',
               4: 'Showdown' }

class HandRank(IntEnum):
    HIGH_CARD = auto()
    PAIR = auto()
    TWO_PAIR = auto()
    TRIPS = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    HOUSE = auto()
    QUADS = auto()
    STFU = auto()
    ROYAL = auto()

class Action(IntEnum):
    FOLD = 1
    CALL = 2
    RAISE = 3

class Position(IntEnum):
    IGNORE = -1
    EARLY = 1
    MIDDLE = 2
    LATE = 3
    SB = 4
    BB = 5

HAND_NAME = {HandRank.HIGH_CARD: '{} high',
             HandRank.PAIR: 'pair of {}s',
             HandRank.TWO_PAIR: '{}s and {}s',
             HandRank.TRIPS: 'three {}s',
             HandRank.STRAIGHT: 'straight to the {}',
             HandRank.FLUSH: '{}-high flush',
             HandRank.HOUSE: '{}s full of {}s',
             HandRank.QUADS: 'four {}s',
             HandRank.STFU: '{}-high straight flush',
             HandRank.ROYAL: 'royal flush'}



# Globals
deck = [value + suit for value in VALUES for suit in SUITS]
known = set()
unknown = set(deck)




class Player:
    name = ''
    def __init__(self, v=1, npc=True):
        assert isinstance(npc, bool)
        self.npc = npc
        if not npc:  return

        self.name = '       '
        self.chips = 0
        self.in_game = False
        self.in_hand = False
        self.seen_cards = '       '
        self.button = False
        self.table_pos = None
        self.current_bet = None
        self.side_pot_idx = None
        if v == 1: return

        # TODO: future version variables belong here
        pass


class OtherHolePredictor:
    """
    Figure out all possible combinations of cards from `unknown` and
    likelihood of calling with each combo. For advanced analysis,
    consider each board stage and bet. Return a priority queue with
    a list of likely hole cards and probability of occurrence.
    """
    def __init__(self):
        # TODO
        pass


class DrawFinder:
    def __init__(self, hole_set, board_set, owner=None):
        assert isinstance(hole_set, set)
        assert isinstance(board_set, set)
        assert len(hole_set) == 2
        assert len(board_set) < 5
        self.get_draws(hole_set, board_set)

    def get_draws(self, hole_set, board_set):
        cards_to_go = 5 - len(board_set)
        hole0, hole1 = list(hole_set)
        hole0_v, hole0_s = hole0
        hole1_v, hole1_s = hole1

        pair = hole0_v == hole1_v
        suited = hole0_s == hole1_s
        _dist = abs(VALUES.index(hole0_v) - VALUES.index(hole1_v))
        connectors = _dist == 1 or _dist == 12

        # Identify range of outcomes including best possible
        # TODO

        # Get number of draws to each outcome
        # TODO


class Hand:
    def __init__(self, hand_set, owner=None):
        assert isinstance(hand_set, set)
        assert len(hand_set) == 7
        self.get_value(hand_set, owner=owner)

    def get_value(self, hand_set, owner=None):
        return None

    def __str__(self):
        return "Placeholder Hand"

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def compare(self, other):
        return 0

    def number_of_outs(self):
        pass


class Game:
    def __init__(self, n=5, v=1):
        assert isinstance(n, int)
        assert isinstance(v, int)
        assert n > 1 and n <= 10
        self.betting_round = -1
        self.active_players = n
        self.num_hands = 0
        self.active_bet = None
        self.chips_per_pot = []

        # Create group of players with user-controlled player in the middle
        n -= 1
        mid_idx = n // 2
        self.players = [Player() for _ in range(mid_idx)]
        self.players.append( Player(npc=False) )
        self.me = mid_idx
        self.players += [Player() for _ in range(n - mid_idx)]

        # Give players names, chips, and a dealer button
        for i, player in enumerate(self.players, 1):
            player.in_game = True
            player.button = True if i == 1 else False  # TODO: properly randomize
            player.name = f'Plyr {i:<2}' if player.npc else '  Bob  '
            player.chips = 5000
            player.table_pos = i

        # Circular linked list
        self.players.append(self.players[0])
        for ccw, cw in pairwise(self.players):
            ccw.next = cw
            cw.prev = ccw
        self.players.pop()

        if not self.players[0].button:
            raise RuntimeError('Expected first player in Game.players array to have var button=True')
        self.dealer = self.players[0]

    def remove_player(self, idx):
        assert isinstance(idx, int)
        player_to_remove = self.players[idx]
        assert isinstance(player_to_remove, Player)
        assert player_to_remove.in_game

        playing_behind = player_to_remove.prev
        playing_ahead = player_to_remove.next

        playing_behind.next = playing_ahead
        playing_ahead.prev = playing_behind

        if self.players[idx].button:
            self.players[idx].button = False
            playing_ahead.button = True

        player_to_remove.in_game = False
        self.active_players -= 1

    def play_gui(self):
        self.play(gui=True)

    def play(self, gui=False):
        while self.active_players > 1:
            self.begin_round()
            if not gui:
                self.show_table()  # Pre-flop
            self.get_action()

            if self.advance_round():  continue
            if not gui:
                self.show_table()  # Flop
            self.get_action()

            if self.advance_round():  continue
            if not gui:
                self.show_table()  # Turn
            self.get_action()

            if self.advance_round():  continue
            if not gui:
                self.show_table()  # River
            self.get_action()

            if self.advance_round(): continue
            if not gui:
                self.show_table()  # Showdown
            self.get_action()  # TODO-debug

            self.decide_winner()

    def begin_round(self):
        self.board = []
        self.chips_per_pot = [0]
        reshuffle()
        self.betting_round = 0
        self.num_hands += 1
        if self.num_hands > 1:
            self.dealer.button = False
            self.dealer = self.dealer.next
            self.dealer.button = True

        for player in self.players:
            player.in_hand = True if player.in_game else False
            player.hole_cards = [ draw_card(npc=player.npc), draw_card(npc=player.npc), ]
            player.seen_cards = '       ' if not player.in_hand else '|XX|XX|' if player.npc else f'|{player.hole_cards[0]}|{player.hole_cards[1]}|'

    def show_table_and_get_action(self):
        self.show_table()
        self.get_action()

    def show_table(self):
        print('                                        === ' + ROUND_NAME[self.betting_round] + ' ===      ')
        print('                          Board: ', end='')
        print(self.board)
        print()
        if self.betting_round == 4:
            print('Winner:')
        else:
            print('Action ->')
        print()
        print('         ' + '   '.join(['  (D)  ' if player.button else '       ' for player in self.players]) )
        print('         ' + '   '.join([player.name for player in self.players]) )
        print('         ' + '   '.join([f'{player.chips:^7}' for player in self.players]) )
        print()
        print('         ' + '   '.join([player.seen_cards for player in self.players]) )
        print()

    def get_action(self):
        if self.betting_round == 4:  # TODO-debug
            print()  # TODO-debug
            print()  # TODO-debug
            input()  # TODO-debug
            return  # TODO-debug

        final_player = self.dealer
        current_player = self.dealer.next

        # TODO: this entire thing needs a revamp. If a betting action occurs, final_player and absolute_bet_right_now needs updating.
        absolute_bet_right_now = LIMIT_BET  # TODO-debug
        while True:
            if current_player.npc:
                current_player.check_or_call()  # TODO: implement
            else:
                final_player = current_player.prev
                current_player.bet(LIMIT_BET)  # TODO: implement # TODO: set final_player parameter automatically
            if current_player == final_player:
                break
            current_player = current_player.next

        # TODO: self.chips_per_pot[-1] += sum([player.current_bet for player in self.players])
        for player in self.players:
            player.current_bet = 0

    def advance_round(self):
        num_players = sum([1 if player.in_hand else 0 for player in self.players])
        self.betting_round += 1
        draw_card()  # burn card
        match self.betting_round:
            case 1:
                min_bet, max_bet = LIMIT_BET, LIMIT_BET  # TODO: implement, also change to bet_amt and cap (for limit)?
                self.board.append( draw_card() )
                self.board.append( draw_card() )
                self.board.append( draw_card() )
            case 2:
                min_bet, max_bet = 2 * LIMIT_BET, 2 * LIMIT_BET
                self.board.append( draw_card() )
            case 3:
                min_bet, max_bet = 2 * LIMIT_BET, 2 * LIMIT_BET
                self.board.append( draw_card() )
            case 4:
                for player in self.players:
                    player.seen_cards = '       ' if not player.in_hand else f'|{player.hole_cards[0]}|{player.hole_cards[1]}|'

    def decide_winner(self):
        # TODO: for each player in the outermost pot, test against neighbor until only players with "0" compare remain.
        #   Then, split the pot between these players. Open the next pot and repeat until all cash is settled.

        showdown_pool = [Hand(set(self.board + player.hole_cards), owner=player) for player in self.players if player.in_hand]
        i = 0
        while i < len(showdown_pool) - 1:
            outcome = showdown_pool[i].compare(showdown_pool[i+1])
            if outcome > 0:
                showdown_pool.pop(i+1)
            elif outcome < 0:
                for _ in range(i+1):
                    showdown_pool.pop(0)
            else:
                i += 1

        print([hand.owner.name for hand in showdown_pool])
        print([str(hand) for hand in showdown_pool])  # TODO-debug

        chips_per_shove, total_odd_chips = divmod(self.chips_per_pot[-1], len(showdown_pool))
        for gets_odd, hand in enumerate(showdown_pool):
            hand.owner.chips += chips_per_shove + (1 if gets_odd < total_odd_chips else 0)


def reshuffle():
    global from_deck
    assert len(deck) == 52
    known = set()
    unknown = set(deck)
    shuffle(deck)
    from_deck = iter(deck)


def draw_card(npc=False):
    global known, unknown
    card = next(from_deck)
    if not npc:
        known |= set(card)
        unknown -= set(card)
    return card


def card_name(card):
    assert isinstance(card, str)
    assert len(card) == 2
    value, suit = card
    assert value in VALUES
    assert suit in SUITS
    return f'{VALUE_NAME[value]} of {SUIT_NAME[suit]}s'


if __name__ == '__main__':
    game = Game(n=10, v=1)
    game.play()
