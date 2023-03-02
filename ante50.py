# TODO
# ====
# Close up existing TODO tags
# Side pots (and odd chips)
# Arrays (n=2..10) containing ideal starting hand strength
# Strategy class
# - (per round)
# - (per opponent)
# - (per situation)
# - (per current hand)
# - to start: fold/call/raise percentage with per-round inertia
# - (integer versions: start with 1)
# Stats
# - win/loss hand count
# - win/loss cash amount
# - per round: number of folds, calls, raises
# Player class
# - avail cash
# - hand history as stats class
# - strategy as strategy class
# Game class
# - stakes, incl. limit/no-limit/in between
# - players
# - handle each round
# - get input
# Provide modifiable stats as a JSON (with min version for each stat, for backwards compat)
# Decision maker (strategy) is imported and called


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


class Stats:
    def __init__(self, v=1):
        if v < 1 or v > MAX_VER:
            raise ValueError(f'Invalid version argument provided to Strategy class: {v}')

        hands_won  = [0, 0, 0, 0]
        hands_lost = [0, 0, 0, 0]
        chips_won  = [0, 0, 0, 0]
        chips_lost = [0, 0, 0, 0]
        num_folds  = [0, 0, 0, 0]
        num_calls  = [0, 0, 0, 0]
        num_raises = [0, 0, 0, 0]
        if v == 1:  return

        # TODO: future version variables belong here
        pass


class Strategy:
    def __init__(self, v=1):
        if v < 1 or v > MAX_VER:
            raise ValueError(f'Invalid version argument provided to Strategy class: {v}')

        self.stddev_perfect_hole_selection = 0.5
        self.stddev_perfect_bet = [0, 0, 0, 0]
        self.position_awareness_frac = 0.8  # 0.0 to 1.0, higher is more aware

        self.strength_table = [
                #A K Q J T 9 8 7 6 5 4 3 2 (suited)
                [8,8,7,7,6,4,4,4,4,4,4,4,4], # A
                [7,8,7,6,5,3,2,2,2,2,2,2,2], # K
                [6,5,8,6,5,4,2,0,0,0,0,0,0], # Q
                [5,4,4,8,6,5,3,1,0,0,0,0,0], # J
                [3,3,3,4,7,5,4,2,0,0,0,0,0], # T
                [1,1,1,2,2,6,5,4,1,0,0,0,0], # 9
                [0,0,0,1,1,2,5,4,3,1,0,0,0], # 8
                [0,0,0,0,0,0,1,4,4,3,1,0,0], # 7
                [0,0,0,0,0,0,0,1,3,2,2,0,0], # 6
                [0,0,0,0,0,0,0,0,1,3,3,2,0], # 5
                [0,0,0,0,0,0,0,0,0,1,2,2,1], # 4
                [0,0,0,0,0,0,0,0,0,0,0,2,1], # 3
                [0,0,0,0,0,0,0,0,0,0,0,0,2]] # 2
                # (off-suit)

        circumstance_and_modification = [('False', 'pass'),]  # TODO

        if v == 1:  return

        # TODO: future version variables belong here
        pass


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
        self.stats = Stats(v=v)
        self.strategy = Strategy(v=v)
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
        assert owner is None or isinstance(owner, Player)
        self.owner = owner

        value_cnt, suit_cnt = map(Counter, zip(*hand_set))
        assert all([value in VALUES for value in value_cnt])
        assert all([suit in SUITS for suit in suit_cnt])

        self.hand_set = hand_set
        self.strength = HandRank.HIGH_CARD

        names = lambda ia: [VALUE_NAME[VALUES[i]] for i in ia]

        # Check for flush
        common_suit, n_suited = suit_cnt.most_common(1)[0]
        if n_suited >= 5:
            self.strength = HandRank.FLUSH
            self.highest_cards = [VALUE_NAME[VALUES[max([VALUES.index(value) for value, suit in hand_set if suit == common_suit])]]]
            value, suit = zip(*hand_set)
            sorted_suit_idxs = sorted([VALUES.index(value) for value, suit in hand_set if suit == common_suit])
            self.rank = list(reversed(sorted_suit_idxs))[0:5]

        # Check for repeated values (pair, two pair, three of a kind, full house, four of a kind)
        top_values, top_counts = list(zip(*value_cnt.most_common()))  # Get counts for repeated cards
        top_card_idxs = [VALUES.index(value) for value in top_values]
        while True:
            if top_counts[0] == 4:  # 4-3 or 4-2-1 or 4-1-1-1
                self.strength = HandRank.QUADS
                self.rank = top_card_idxs[0:1] + list(reversed(sorted(top_card_idxs[1:])))[0:1]
                break
            if top_counts[0] == 3:
                if top_counts[1] >= 2:
                    self.strength = HandRank.HOUSE
                    if top_counts[1] == 2:
                        if top_counts[2] == 2:  # 3-2-2
                            self.rank = top_card_idxs[0:1] + list(reversed(sorted(top_card_idxs[1:3])))
                        else:  # 3-2-1-1
                            self.rank = top_card_idxs
                    else:  # 3-3-1
                        self.rank = list(reversed(sorted(top_card_idxs[0:2])))
                else:  # 3-1-1-1-1
                    self.strength = max(self.strength, HandRank.TRIPS)
                    self.rank = top_card_idxs[0:1] + list(reversed(sorted(top_card_idxs[1:])))[1:4]
                break
            if self.strength == HandRank.FLUSH:
                break
            if top_counts[0] == 2:
                if top_counts[1] == 2:
                    self.strength = HandRank.TWO_PAIR
                    if top_counts[2] == 2:  # 2-2-2-1
                        pairs_ranked = list(reversed(sorted(top_card_idxs[0:3])))
                        self.rank = pairs_ranked[0:2] + list(reversed(sorted(pairs_ranked[2:3] + top_card_idxs[3:4])))[0:1]
                    else:  # 2-2-1-1-1
                        self.rank = list(reversed(sorted(top_card_idxs[0:2]))) + list(reversed(sorted(top_card_idxs[2:])))[0:1]
                else:  # 2-1-1-1-1-1
                    self.strength = HandRank.PAIR
                    self.rank = top_card_idxs[0:1] + list(reversed(sorted(top_card_idxs[1:])))[0:3]
            break

        # Check for straights and straight flushes
        if self.strength <= HandRank.FLUSH:
            baby_straight = len([True for value in list(value_cnt) if value in WHEEL]) == 5
            value_idxs = sorted([VALUES.index(v) for v in list(value_cnt)])
            d_value_idxs = ''.join([str(b-a) for (a, b) in pairwise(value_idxs)])  # Conversion to string is slow but easy
            best_match_idx = d_value_idxs.rfind('1111')
            if best_match_idx >= 0 or baby_straight:
                if self.strength < HandRank.FLUSH:
                    self.strength = HandRank.STRAIGHT
                    self.rank = [3] if baby_straight and best_match_idx == -1 else [value_idxs[best_match_idx+4]]
                else:
                    # Straight and flush in hand, so test if straight flush or simply flush
                    steel_wheel = len([True for idx in sorted_suit_idxs if VALUES[idx] in WHEEL]) == 5
                    d_sorted_suit_idxs = ''.join([str(b-a) for (a, b) in pairwise(sorted_suit_idxs)])
                    best_match_idx = d_sorted_suit_idxs.rfind('1111')
                    if best_match_idx >= 0 or steel_wheel:
                        print(sorted_suit_idxs)
                        self.strength = HandRank.STFU if steel_wheel or sorted_suit_idxs[best_match_idx+4] < 12 else HandRank.ROYAL
                        self.rank = [3] if steel_wheel and best_match_idx == -1 else [sorted_suit_idxs[best_match_idx+4]]

        # Get high card
        if self.strength == HandRank.HIGH_CARD:
            self.rank = list(reversed(sorted(top_card_idxs)))[0:5]

        self.highest_cards = names(self.rank)

    def __str__(self):
        return HAND_NAME[self.strength].format(*self.highest_cards).replace('sixs','sixes')

    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    def compare(self, other):
        assert isinstance(other, Hand)
        assert len(self.hand_set | other.hand_set) == 9
        assert len(self.hand_set & other.hand_set) == 5

        if self.strength != other.strength:
            return 1 if self.strength > other.strength else -1
        if self.rank == other.rank:
            return 0
        return 1 if self.rank > other.rank else -1

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

    def play(self):
        while self.active_players > 1:
            self.begin_round()
            self.show_table_and_get_action()  # Pre-flop

            if self.advance_round():  continue
            self.show_table_and_get_action()  # Flop

            if self.advance_round():  continue
            self.show_table_and_get_action()  # Turn

            if self.advance_round():  continue
            self.show_table_and_get_action()  # River

            if self.advance_round(): continue
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
            player.hole_cards = [ draw_card(npc=npc), draw_card(npc=npc), ]
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

        while True:
            if current_player.npc:
                action = current_player.strategy.get_action()
                if action == Action.FOLD:
                    if current_player.current_bet < absolute_bet_right_now:
                        current_player.fold()  # TODO: belongs somewhere else?
                    else:
                        check()
                elif action == Action.CALL:
                    current_player.current_bet = absolute_bet_right_now
                elif action == Action.RAISE:
                    if absolute_bet_right_now < betting_cap:
                        current_player.current_bet = LIMIT_BET + absolute_bet_right_now # TODO
                        current_player.chips -= LIMIT_BET  # TODO: this should happen when the bet occurs
            else:
                print('1 - fold   2 - check/call   3 - bet/raise   q - quit', end='\n\n')
                #print('1 - fold   2 - check/call   3 - bet/raise   ~ - next hand (debug)', end='\n\n')
                decision = ''
                while len(decision) != 1 or decision not in '123q~':
                    print(CURSOR_UP + ' '*len(decision) + '\r', end='')
                    decision = input()
                me = self.players[self.me]
                match decision:
                    case '1':
                        me.in_hand = False
                        me.seen_cards = '       '
                        pass
                    case '2':
                        me.current_bet = LIMIT_BET  # TODO
                        me.chips -= LIMIT_BET
                        pass
                    case '3':
                        pass
                    case 'q':
                        import sys
                        sys.exit(0)
                    ### case '~':
                    ###     for player in self.players:
                    ###         player.in_hand = False
                    ###     self.betting_round = -1  # TODO-hi: fix this, and this is also needed for when everyone folds early
            if current_player == final_player:
                break
            current_player = current_player.next

        self.chips_per_pot[-1] += sum([player.current_bet for player in self.players])
        for player in self.players:
            player.current_bet = 0

        print(CURSOR_UP * 14)

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
