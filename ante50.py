# TODO
# ====
# Close up existing TODO tags
# Function to sort by card value (instead of calling VALUES[sorted(VALUES.index(v))])

# TODO: put docstrings for each major code block:
# Strategy class
# - currently, only implements position-agnostic pre-flop hand strength for a full table
# Stats
# - win/loss hand count
# - win/loss cash amount
# - per round: number of folds, calls, raises
# Player class
# - avail cash
# Game class
# - limit stakes for now
# - players
# - handle each round
# - get input



# Imports
from collections import Counter
from enum import IntEnum
from itertools import pairwise
from random import shuffle


# Consts
MAX_VER = 1
LIMIT_BET = 2
SHOW_ROUNDS = False
STATS_ONLY = False
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

class Round(IntEnum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4

ROUND_NAME = { Round.PREFLOP: 'Pre-flop',
               Round.FLOP: 'Flop',
               Round.TURN: 'Turn',
               Round.RIVER: 'River',
               Round.SHOWDOWN: 'Showdown' }

class HandRank(IntEnum):
    HIGH_CARD = 0
    PAIR      = 1
    TWO_PAIR  = 2
    TRIPS     = 3
    STRAIGHT  = 4
    FLUSH     = 5
    HOUSE     = 6
    QUADS     = 7
    STFU      = 8
    ROYAL     = 9

class Action(IntEnum):
    UNDECIDED = 0
    CHECK_OR_FOLD = 1
    CHECK_OR_CALL = 2
    RAISE_OR_CALL = 3
    FOLD = 4
    CHECK = 5
    CALL = 6
    RAISE = 7

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
    def __init__(self):
        # Indexes:
        # 0 = during pre-flop betting
        # 1 = during flop betting
        # 2 = during turn betting
        # 3 = during river betting
        # 4 = after showdown
        self.hands_won  = [0, 0, 0, 0, 0]
        self.hands_lost = 0
        self.chips_won  = [0, 0, 0, 0, 0]
        self.chips_lost = [0, 0, 0, 0, 0]
        self.num_folds  = [0, 0, 0, 0, 0]
        self.num_calls  = [0, 0, 0, 0, 0]
        self.num_raises = [0, 0, 0, 0, 0]
        self.winning_hand_type = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.losing_hand_type = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.allin_hands_won_lost = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.allin_chips_won_lost = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

        all_hole_strs = [VALUES[x] + VALUES[y] for x in range(13) for y in range(x+1)] + \
                        [VALUES[x] + VALUES[y] + 's' for x in range(13) for y in range(x)]

        self.hole_str_cnt = Counter({k: 0 for k in all_hole_strs})

    def print_stats(self):
        print(f'Hands played: {self.total_hands()}')
        print(f'  Hands won: {sum(self.hands_won)} ({self.hands_won[Round.SHOWDOWN]} at showdown)')
        print(f'  Hands lost: {self.hands_lost}')
        print(f'  Hands folded: {sum(self.num_folds)}')
        print(f'Raises: {sum(self.num_raises)}')
        print(f'Balance: {sum(self.chips_won) - sum(self.chips_lost)}')
        print(f'  Cash won: {sum(self.chips_won)}')
        print(f'  Cash lost: {sum(self.chips_lost)}')
        print('-----')
        print(f'EV: {self.calculate_ev():.3f} big blinds / hand')
        print(f'WINNING HAND HISTOGRAM: {self.winning_hand_type}')
        ### print(f'LOSING HAND HISTOGRAM: {self.losing_hand_type}')
        ### 
        ### self.print_hole_str_cnt()

    def print_hole_str_cnt(self):
        for j, x in enumerate(reversed(VALUES)):
            for i, y in enumerate(reversed(VALUES)):
                s = x + y + 's' if i > j else y + x
                print(f'{s:<10}', end='')
            print()
            for i, y in enumerate(reversed(VALUES)):
                s = x + y + 's' if i > j else y + x
                print(f'{self.hole_str_cnt[s]:<10}', end='')
            print()
            print()

    def total_hands(self):
        return sum(self.hands_won) + self.hands_lost + sum(self.num_folds)

    def calculate_ev(self):
        ''' Big blinds per hand '''
        total_hands = self.total_hands()
        if total_hands == 0:
            return 0
        profit_or_loss = sum(self.chips_won) - sum(self.chips_lost)
        profit_or_loss_bb = profit_or_loss / LIMIT_BET
        return profit_or_loss_bb / total_hands


class Strategy:
    def __init__(self):
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

    def get_preflop_action(self, hole_str):
        assert isinstance(hole_str, str)
        assert len(hole_str) == 2 or len(hole_str) == 3 and hole_str[2] == 's'
        assert all([v in VALUES for v in hole_str[0:2]])

        suited = True if len(hole_str) == 3 else False

        i = 12 - VALUES.index(hole_str[0])
        j = 12 - VALUES.index(hole_str[1])
        i, j = (i, j) if suited else (j, i)

        match self.strength_table[i][j]:
            case 8 | 7 | 6 | 5:
                return Action.RAISE_OR_CALL
            case 4:
                return Action.CHECK_OR_CALL
            case 4 | 3 | 2 | 1 | 0:
                return Action.CHECK_OR_FOLD
            case _:
                raise RuntimeError('strength_table has an unexpected value')  # TODO: make this error better


class Player:
    name = ''
    def __init__(self, npc=True):
        assert isinstance(npc, bool)
        self.npc = npc
        if not npc:  return

        self.name = '       '
        self.chips = 0
        self.in_game = False
        self.in_hand = False
        self.hole_cards = None
        self.seen_cards = '       '
        self.button = False
        self.cumul_bet = None
        self.current_bet = None

    def hole_str(self):
        assert isinstance(self.hole_cards, list)
        assert len(self.hole_cards) == 2
        assert all([isinstance(e, str) for e in self.hole_cards])
        assert all([len(e) == 2 for e in self.hole_cards])
        assert self.hole_cards[0] != self.hole_cards[1]

        values, suits = zip(*self.hole_cards)

        out_str = ''.join([VALUES[i] for i in sorted([VALUES.index(v) for v in values], reverse=True)])
        out_str += 's' if suits[0] == suits[1] else ''

        return out_str


class Hand:
    def __init__(self, hand_set, owner=None):
        assert isinstance(hand_set, set)
        assert len(hand_set) == 7
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
            sorted_suit_idxs = sorted([VALUES.index(value) for value, suit in hand_set if suit == common_suit])  # TODO: probably use reverse=True
            self.rank = list(reversed(sorted_suit_idxs))[0:5]

        # Check for repeated values (pair, two pair, three of a kind, full house, four of a kind)
        top_values, top_counts = list(zip(*value_cnt.most_common()))  # Get counts for repeated cards
        top_card_idxs = [VALUES.index(value) for value in top_values]
        while True:
            if top_counts[0] == 4:  # 4-3 or 4-2-1 or 4-1-1-1
                self.strength = HandRank.QUADS
                self.rank = top_card_idxs[0:1] + list(sorted(top_card_idxs[1:], reverse=True))[0:1]
                break
            if top_counts[0] == 3:
                if top_counts[1] >= 2:
                    self.strength = HandRank.HOUSE
                    if top_counts[1] == 2:
                        if top_counts[2] == 2:  # 3-2-2
                            self.rank = top_card_idxs[0:1] + list(sorted(top_card_idxs[1:3], reverse=True))[0:1]
                        else:  # 3-2-1-1
                            self.rank = top_card_idxs[0:2]
                    else:  # 3-3-1
                        self.rank = list(sorted(top_card_idxs[0:2], reverse=True))[0:2]
                else:  # 3-1-1-1-1
                    if self.strength == HandRank.FLUSH:
                        break
                    self.strength = max(self.strength, HandRank.TRIPS)
                    self.rank = top_card_idxs[0:1] + list(sorted(top_card_idxs[1:], reverse=True))[0:2]
                break
            if self.strength == HandRank.FLUSH:
                break
            if top_counts[0] == 2:
                if top_counts[1] == 2:
                    self.strength = HandRank.TWO_PAIR
                    if top_counts[2] == 2:  # 2-2-2-1
                        pairs_ranked = list(sorted(top_card_idxs[0:3], reverse=True))
                        self.rank = pairs_ranked[0:2] + list(sorted(pairs_ranked[2:3] + top_card_idxs[3:4], reverse=True))[0:1]
                    else:  # 2-2-1-1-1
                        self.rank = list(sorted(top_card_idxs[0:2], reverse=True)) + list(sorted(top_card_idxs[2:], reverse=True))[0:1]
                else:  # 2-1-1-1-1-1
                    self.strength = HandRank.PAIR
                    self.rank = top_card_idxs[0:1] + list(sorted(top_card_idxs[1:], reverse=True))[0:3]
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
                        self.strength = HandRank.STFU if steel_wheel or sorted_suit_idxs[best_match_idx+4] < 12 else HandRank.ROYAL
                        self.rank = [3] if steel_wheel and best_match_idx == -1 else [sorted_suit_idxs[best_match_idx+4]]

        # Get high card
        if self.strength == HandRank.HIGH_CARD:
            self.rank = list(sorted(top_card_idxs, reverse=True))[0:5]

        self.highest_cards = names(self.rank)

        match self.strength:
            case HandRank.HIGH_CARD:
                assert len(self.rank) == 5
            case HandRank.PAIR:
                assert len(self.rank) == 4
            case HandRank.TWO_PAIR:
                assert len(self.rank) == 3
            case HandRank.TRIPS:
                assert len(self.rank) == 3
            case HandRank.STRAIGHT:
                assert len(self.rank) == 1
            case HandRank.FLUSH:
                assert len(self.rank) == 5
            case HandRank.HOUSE:
                assert len(self.rank) == 2
            case HandRank.QUADS:
                assert len(self.rank) == 2
            case HandRank.STFU:
                assert len(self.rank) == 1
            case HandRank.ROYAL:
                assert len(self.rank) == 1
            case _:
                assert False

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

        for s, o in zip(self.rank, other.rank):
            if s > o:
                return 1
            if s < o:
                return -1
        return 0


class Game:
    def __init__(self, players=5, hands=-1):
        assert isinstance(players, int)
        assert isinstance(hands, int)
        assert players > 1 and players <= 10

        self.winners = None
        self.betting_round = -1
        self.bet_amt = 0
        self.bet_cap = 0
        self.round_not_finished = None
        self.num_hands = 0
        self.target_num_hands = hands
        self.num_active_players = players
        self.acting_player = None
        self.last_player_to_decide = None
        self.high_bet_per_round = []
        self.high_bet = None

        # Create group of players with user-controlled player in the middle
        players -= 1
        mid_idx = players // 2
        self.players = [Player() for _ in range(mid_idx)]
        self.players.append( Player(npc=False) )
        self.me = self.players[mid_idx]
        self.players += [Player() for _ in range(players - mid_idx)]

        # Give players names, chips, and a dealer button
        for i, player in enumerate(self.players, 1):
            player.in_game = True
            player.button = True if i == 1 else False
            player.name = f'Plyr {i:<2}' if player.npc else '  Bob  '
            player.chips = 6 * LIMIT_BET + 1

        # Circular linked list
        self.players.append(self.players[0])
        for ccw, cw in pairwise(self.players):
            ccw.next = cw
            cw.prev = ccw
        self.players.pop()

        if not self.players[0].button:
            raise RuntimeError('Expected first player in Game.players array to have var button=True')
        self.dealer = self.players[0]

    def remove_player(self, player_to_remove):
        assert isinstance(player_to_remove, Player)
        assert player_to_remove.in_game

        playing_behind = player_to_remove.prev
        playing_ahead = player_to_remove.next

        playing_behind.next = playing_ahead
        playing_ahead.prev = playing_behind

        if player_to_remove.button:
            player_to_remove.button = False
            playing_ahead.button = True

        player_to_remove.in_game = False
        self.num_active_players -= 1

    def play(self):
        while self.num_active_players > 1 and self.num_hands != self.target_num_hands and self.me.in_game:
            self.begin_round()
            self.show_round()  # Pre-flop
            self.get_action()
            self.show_action()

            self.advance_round()
            self.show_round()  # Flop
            self.get_action()
            self.show_action()

            self.advance_round()
            self.show_round()  # Turn
            self.get_action()
            self.show_action()

            self.advance_round()
            self.show_round()  # River
            self.get_action()
            self.show_action()

            self.advance_round()
            self.decide_winner()
            self.show_round(always=True)  # Showdown

        #raise RuntimeError('TODO: exited because target_num_hands reached or num_active_players == 1; declare the game winner here')


    def update_bet(self, amount):
        assert isinstance(amount, int)
        assert amount > 0

        chips_avail = max(0, self.acting_player.chips - sum(self.high_bet_per_round))
        self.acting_player.current_bet = chips_avail if chips_avail < amount else amount
        self.acting_player.cumul_bet = sum(self.high_bet_per_round) + self.acting_player.current_bet

    def put_bets_into_pot(self):
        self.high_bet_per_round.append(self.high_bet)
        self.high_bet = 0
        for player in self.players:
            player.current_bet = 0

    def fold_player(self):
        assert self.acting_player.in_hand == True
        self.acting_player.seen_cards = ' fold  '
        self.acting_player.in_hand = False

    def begin_round(self):
        ### assert sum([p.chips for p in self.players]) == 2000  # TODO-debug
        self.round_not_finished = True
        self.num_hands += 1
        self.board = []
        self.winners = None
        self.betting_round = 0
        self.bet_amt, self.bet_cap = LIMIT_BET, 4 * LIMIT_BET

        if self.num_hands > 1:
            self.advance_button()

        if self.num_active_players > 2:
            self.acting_player = self.dealer.next
        else:
            self.acting_player = self.dealer
        self.update_bet(self.bet_amt // 2)  # Small blind
        self.acting_player = self.acting_player.next
        self.update_bet(self.bet_amt)  # Big blind
        self.acting_player = self.acting_player.next

        self.high_bet = self.bet_amt  # needed for when big blind does not have enough chips
        self.high_bet_per_round = []

        reshuffle()
        for player in self.players:
            # ... and deal
            player.in_hand = True if player.in_game else False
            player.cumul_bet = 0
            player.current_bet = 0
            if player.in_hand:
                player.hole_cards = [ draw_card(npc=player.npc), draw_card(npc=player.npc), ]
                player.seen_cards = '|XX|XX|' if player.npc else f'|{player.hole_cards[0]}|{player.hole_cards[1]}|'
            else:
                player.hole_cards = None
                player.seen_cards = '       '

    def advance_button(self):
        self.dealer.button = False
        self.dealer = self.dealer.next
        self.dealer.button = True

    def show_round(self, always=False):
        if not always and not SHOW_ROUNDS:
            return
        if STATS_ONLY:
            return
        print('                                        === ' + ROUND_NAME[self.betting_round] + ' ===      ')
        print('                          Board: ', end='')
        print(self.board)
        print()
        print('         ' + '   '.join(['  (D)  ' if player.button else '       ' for player in self.players]) )
        print('         ' + '   '.join([player.name for player in self.players]) )
        print('         ' + '   '.join([f'{player.chips-player.cumul_bet:^7}' for player in self.players]) )
        print()
        print('         ' + '   '.join([player.seen_cards for player in self.players]) )
        print()
        if self.betting_round == 4:
            winner_str = ' and '.join([w.strip() for w in self.winners[0]]) + ' with '
            if self.winners[1][0][-1] != 's' or self.winners[1][0][0] == 'p':
                if self.winners[1][0][0] == 'a' and self.winners[1][0][3] != 's' or self.winners[1][0][0] == 'e' and self.winners[1][0][5] != 's':
                    winner_str += 'an '
                else:
                    winner_str += 'a '
            winner_str += self.winners[1][0]
            print(f'Winner: {winner_str}')
        print()

    def show_action(self, always=False):
        if not always and not SHOW_ROUNDS:
            return
        if STATS_ONLY:
            return
        print('Action ->   ' + '         '.join([str(p.current_bet) for p in self.players]))

    def execute(self, action):
        assert isinstance(action, Action)

        # TODO: skip action and jump to last_player_to_decide check if a player is all-in
        chips_avail = max(0, self.acting_player.chips - sum(self.high_bet_per_round))
        allin = False if chips_avail else True
        if not allin:

            match action:
                case Action.CHECK_OR_FOLD:
                    decision = Action.CHECK if self.high_bet == self.acting_player.current_bet else Action.FOLD
                case Action.CHECK_OR_CALL:
                    decision = Action.CHECK if self.high_bet == self.acting_player.current_bet else Action.CALL
                case Action.RAISE_OR_CALL:
                    decision = Action.CALL if self.high_bet == self.bet_cap else Action.RAISE
                case _:
                    raise ValueError(f'"action" argument provided to execute() ({action.name}) is disallowed')

            match decision:
                case Action.FOLD:
                    self.fold_player()
                case Action.CHECK:
                    pass
                case Action.CALL:
                    if self.high_bet > 0:
                        self.update_bet(self.high_bet)
                case Action.RAISE:
                    bob_stats.num_raises[self.betting_round] += 1
                    if not self.high_bet:  # Bet
                        self.high_bet = min(chips_avail, self.bet_amt)
                    else:  # Raise
                        self.high_bet = min([chips_avail, self.bet_cap, self.high_bet + self.bet_amt])
                    self.update_bet(self.high_bet)
                    self.last_player_to_decide = self.acting_player.prev

        if self.acting_player == self.last_player_to_decide:
            self.round_not_finished = False
            return

        self.acting_player = self.acting_player.next

    def get_action(self):
        assert self.betting_round < 4

        if self.betting_round > 0:
            self.acting_player = self.dealer.next

        self.last_player_to_decide = self.acting_player.prev

        # TODO: fix betting, chip values
        while self.round_not_finished:
            if self.acting_player.npc:
                action = Action.CHECK_OR_CALL
            else:
                hole_str = self.acting_player.hole_str()
                action = preflop_strat.get_preflop_action(hole_str)
            self.execute(action)

    def advance_round(self):
        # TODO: num_active_players ... num_players = sum([1 if player.in_hand else 0 for player in self.players])
        self.put_bets_into_pot()
        self.betting_round += 1
        if self.betting_round < Round.SHOWDOWN:
            draw_card()  # burn card
        match self.betting_round:
            case Round.FLOP:
                self.bet_amt, self.bet_cap = LIMIT_BET, 4 * LIMIT_BET
                self.board.append( draw_card() )
                self.board.append( draw_card() )
                self.board.append( draw_card() )
            case Round.TURN:
                self.bet_amt, self.bet_cap = 2 * LIMIT_BET, 8 * LIMIT_BET
                self.board.append( draw_card() )
            case Round.RIVER:
                self.bet_amt, self.bet_cap = 2 * LIMIT_BET, 8 * LIMIT_BET
                self.board.append( draw_card() )
            case Round.SHOWDOWN:
                for player in self.players:
                    if player.in_game:
                        player.seen_cards = ' fold  ' if not player.in_hand else f'|{player.hole_cards[0]}|{player.hole_cards[1]}|'

        if self.betting_round == Round.SHOWDOWN:
            return

        self.round_not_finished = True

    def decide_winner(self):
        # TODO: for each player in the outermost pot, test against neighbor until only players with "0" compare remain.
        #   Then, split the pot between these players. Open the next pot and repeat until all cash is settled.

        pot_order_highest_first = sorted(set([p.cumul_bet for p in self.players]), reverse=True)
        if pot_order_highest_first[-1] != 0:
            pot_order_highest_first.append(0)
        incremental_pot_amount = [hi-lo for (hi, lo) in pairwise(pot_order_highest_first)]

        for player in self.players:
            player.chips -= player.cumul_bet

        for incr, chip_amt in zip(incremental_pot_amount, pot_order_highest_first):
            showdown_pool = [Hand(set(self.board + player.hole_cards), owner=player) for player in self.players if player.cumul_bet >= chip_amt and player.in_hand]
            pot_amount = sum([incr for player in self.players if player.cumul_bet >= chip_amt])

            i = 0
            while i < len(showdown_pool) - 1:
                outcome = showdown_pool[i].compare(showdown_pool[i+1])
                if outcome > 0:
                    hd = showdown_pool.pop(i+1)
                    hd.owner.in_hand = False if hd.owner != self.me else True  # TODO-debug: left in for stats
                elif outcome < 0:
                    for _ in range(i+1):
                        hd = showdown_pool.pop(0)
                        hd.owner.in_hand = False if hd.owner != self.me else True  # TODO-debug: left in for stats
                    i = 0
                else:
                    i += 1

            chips_per_shove, total_odd_chips = divmod(pot_amount, len(showdown_pool))

            for gets_odd, hand in enumerate(showdown_pool):
                hand.owner.chips += chips_per_shove + (1 if gets_odd < total_odd_chips else 0)
                if hand.owner == self.me:
                    bob_stats.chips_won[Round.SHOWDOWN] += chips_per_shove + (1 if gets_odd < total_odd_chips else 0) - incr


        self.winners = [[hand.owner.name for hand in showdown_pool], [str(hand) for hand in showdown_pool],]

        # TODO-debug
        my_hand = Hand(set(self.board + self.me.hole_cards))

        # TODO-debug
        # TODO: fix stats for winning after opponents fold
        has_won = True if self.me in [hand.owner for hand in showdown_pool] else False
        if has_won:
            bob_stats.num_calls = [n+1 for n in bob_stats.num_calls]
            bob_stats.hands_won[Round.SHOWDOWN] += 1
            bob_stats.winning_hand_type[my_hand.strength] += 1
        elif self.me.in_hand:
            bob_stats.hands_lost += 1
            bob_stats.chips_lost[Round.SHOWDOWN] += self.me.cumul_bet
            bob_stats.losing_hand_type[my_hand.strength] += 1
        else:  # folded
            bob_stats.num_folds[Round.PREFLOP] += 1
        bob_stats.hole_str_cnt[self.me.hole_str()] += 1

        for player in self.players:
            player.cumul_bet = 0  # Added so showdown appears correctly
            if player.in_game and player.chips == 0:
                self.remove_player(player)
            elif player.chips < 0:
                raise RuntimeError('A player is playing on credit. This is strictly forbidden!')


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
    preflop_strat = Strategy()
    bob_stats = Stats()
    game = Game(players=4, hands=3000)
    game.play()
    bob_stats.print_stats()
    ### print(f'# rounds: {game.num_hands}')  # TODO-debug: check that this matches bob_stats

