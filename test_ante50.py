from ante50 import Game, Hand, Strategy, reshuffle, draw_card, card_name

import pytest


def test_strategy_class():
    with pytest.raises(ValueError):
        Strategy(v=0)
    s = Strategy(v=1)
    assert s.position_awareness_frac == 0.8


def test_hand_failures():
    with pytest.raises(AssertionError):
        Hand(set([]))  # empty set (too short)
    with pytest.raises(AssertionError):
        Hand(set(['5h']))  # too short
    with pytest.raises(AssertionError):
        Hand(set(['2h','3c','4d','5h','7s','8c']))  # too short
    with pytest.raises(AssertionError):
        Hand(set(['2c','3c','4c','5c','6c','7c','8c','9c']))  # too long
    with pytest.raises(AssertionError):
        Hand(['2c','3c','4c','5c','6c','7c','8c'])  # not a set
    with pytest.raises(AssertionError):
        Hand({'2c':0,'3c':1,'4c':2,'5c':3,'6c':4,'7c':5,'8c':6})  # not a set
    with pytest.raises(AssertionError):
        Hand(None)  # not a set
    with pytest.raises(AssertionError):
        Hand(set(['2h','3c','4x','5h','7s','8c','9c']))  # false suit
    with pytest.raises(AssertionError):
        Hand(set(['2h','3c','4c','5h','1s','8c','9c']))  # false value


def test_hand_names():
    assert str(Hand(set(['2h','3c','4d','5h','7s','8c','9c']))) == 'nine high'
    assert str(Hand(set(['8h','9c','4d','5h','7s','3c','2h']))) == 'nine high'  # out-of-order
    assert str(Hand(set(['2h','3c','4d','7h','8s','9h','Tc']))) == 'ten high'
    assert str(Hand(set(['2h','Jc','4d','5h','8s','9h','Tc']))) == 'jack high'
    assert str(Hand(set(['2h','3c','4d','Qh','8s','9h','Th']))) == 'queen high'
    assert str(Hand(set(['2h','3c','Ks','Qh','8s','9c','Tc']))) == 'king high'
    assert str(Hand(set(['Ah','3c','Ks','Qh','8s','9c','Tc']))) == 'ace high'
    assert str(Hand(set(['Ah','7h','Kh','Qh','Jc','9c','8c']))) == 'ace high'  # four hearts
    assert str(Hand(set(['3h','5c','Js','Th','2s','7h','2d']))) == 'pair of deuces'
    assert str(Hand(set(['3d','3c','Ks','Qh','8s','9d','Tc']))) == 'pair of treys'
    assert str(Hand(set(['3d','4c','4s','Qh','8s','9d','Tc']))) == 'pair of fours'
    assert str(Hand(set(['3d','5c','4s','Qh','8s','5h','Tc']))) == 'pair of fives'
    assert str(Hand(set(['3d','5c','4s','6h','8s','6c','Tc']))) == 'pair of sixes'
    assert str(Hand(set(['7d','7c','4s','Qh','8s','5h','Tc']))) == 'pair of sevens'
    assert str(Hand(set(['3d','8c','4s','Qh','8s','5h','Tc']))) == 'pair of eights'
    assert str(Hand(set(['3d','Kc','4s','Qh','8s','9h','9c']))) == 'pair of nines'
    assert str(Hand(set(['Td','5c','4s','Qh','Js','8h','Tc']))) == 'pair of tens'
    assert str(Hand(set(['3d','5c','Js','Jh','8s','Ah','Tc']))) == 'pair of jacks'
    assert str(Hand(set(['3d','Qc','4s','Qh','8s','5h','Tc']))) == 'pair of queens'
    assert str(Hand(set(['3d','5c','Ks','Qh','8s','Kh','Tc']))) == 'pair of kings'
    assert str(Hand(set(['Ad','5c','4s','Qh','8s','Ah','Tc']))) == 'pair of aces'
    assert str(Hand(set(['Ad','5d','4d','Qd','8s','Ah','Tc']))) == 'pair of aces'  # 4 diamonds
    assert str(Hand(set(['Ad','5d','4d','Qd','8d','Ah','Tc']))) == 'ace-high flush'  # 5 diamonds
    assert str(Hand(set(['Ad','5c','4c','Qc','8c','Ah','Tc']))) == 'queen-high flush'  # 5 clubs
    assert str(Hand(set(['9h','5h','4h','Qc','8h','Ad','Th']))) == 'ten-high flush'  # 5 hearts
    assert str(Hand(set(['9h','5h','4h','2h','8h','Ad','Th']))) == 'ten-high flush'  # 6 hearts
    assert str(Hand(set(['9h','5h','4h','2h','8h','3h','Th']))) == 'ten-high flush'  # 7 hearts
    assert str(Hand(set(['Ks','5s','4s','Qs','8s','Ah','Tc']))) == 'king-high flush'  # 5 spades
    assert str(Hand(set(['Kh','5s','4s','6s','8s','7h','9s']))) == 'nine-high flush'  # flush with straight
    assert str(Hand(set(['Jd','5c','4s','Jh','8s','5h','Tc']))) == 'jacks and fives'
    assert str(Hand(set(['3d','3c','2s','2h','8s','5h','Tc']))) == 'treys and deuces'
    assert str(Hand(set(['3d','Ac','2s','2h','8s','Ah','Tc']))) == 'aces and deuces'
    assert str(Hand(set(['3d','Ac','2s','2h','8s','Ah','8c']))) == 'aces and eights'
    assert str(Hand(set(['3d','4c','2s','3h','4s','2h','Tc']))) == 'fours and treys'  # 2 deuces
    assert str(Hand(set(['3d','4c','2s','3h','4s','2h','2c']))) == 'deuces full of fours'
    assert str(Hand(set(['3d','5c','2s','3h','4s','2h','2c']))) == 'deuces full of treys'
    assert str(Hand(set(['3d','5c','3s','3h','4s','2h','2c']))) == 'treys full of deuces'
    assert str(Hand(set(['Td','5c','Ts','Th','6s','2h','6c']))) == 'tens full of sixes'
    assert str(Hand(set(['Td','5c','Ts','Th','6s','6h','6c']))) == 'tens full of sixes' # 3 sixes
    assert str(Hand(set(['Td','6d','Ts','Th','6s','6h','6c']))) == 'four sixes'  # 3 tens
    assert str(Hand(set(['3d','6d','6s','Th','Ks','5h','6c']))) == 'three sixes'
    assert str(Hand(set(['3d','6d','3s','Th','Ks','5h','3c']))) == 'three treys'
    assert str(Hand(set(['3d','4c','6s','7h','3s','5h','3c']))) == 'straight to the seven'
    assert str(Hand(set(['3d','4c','6s','7h','Ks','5h','Tc']))) == 'straight to the seven'
    assert str(Hand(set(['3d','4c','2s','7h','As','5h','Tc']))) == 'straight to the five'
    assert str(Hand(set(['3d','4c','2s','5c','As','5h','Tc']))) == 'straight to the five'
    assert str(Hand(set(['3d','4c','2s','5c','As','5h','5s']))) == 'straight to the five'
    assert str(Hand(set(['9d','Tc','Js','5c','Qs','5h','Ks']))) == 'straight to the king'
    assert str(Hand(set(['9d','Tc','Js','Ac','Qs','5h','Ks']))) == 'straight to the ace'
    assert str(Hand(set(['3d','5d','2s','5c','As','5h','5s']))) == 'four fives'
    assert str(Hand(set(['3d','6d','2s','6c','As','6h','6s']))) == 'four sixes'
    assert str(Hand(set(['Qd','6d','Qs','Qc','As','Qh','6s']))) == 'four queens'
    assert str(Hand(set(['3d','5d','2d','4d','Ad','6h','6s']))) == 'five-high straight flush'
    assert str(Hand(set(['3d','5d','2d','4d','Ad','Qd','9d']))) == 'five-high straight flush'
    assert str(Hand(set(['3d','5d','2d','4d','Ad','Qd','6d']))) == 'six-high straight flush'
    assert str(Hand(set(['3d','5d','7d','4d','Ad','Qd','6d']))) == 'seven-high straight flush'
    assert str(Hand(set(['9d','7d','Td','Jd','Kd','Qh','8d']))) == 'jack-high straight flush'
    assert str(Hand(set(['9d','7d','Td','Jd','Kh','Qd','8d']))) == 'queen-high straight flush'  # 6 consecutive suited
    assert str(Hand(set(['9d','7d','Td','Jd','Kd','Qd','8d']))) == 'king-high straight flush'  # 7 consecutive suited
    assert str(Hand(set(['9d','5c','Td','Jd','Kd','Qd','6h']))) == 'king-high straight flush'
    assert str(Hand(set(['Ad','5c','Td','Jd','Kd','Qd','6h']))) == 'royal flush'
    assert str(Hand(set(['Ad','8d','Td','Jd','Kd','Qd','9d']))) == 'royal flush'  # 7 consecutive suited


def test_hand_ranks():
    h = Hand(set(['3d','5c','Js','Jh','8c','Qc','Tc']))  # jacks
    o = Hand(set(['3d','Qc','Js','Qh','8c','5h','Tc']))  # queens
    assert h.compare(o) == -1
    assert o.compare(h) == 1  # bi-directional

    h = Hand(set(['3h','5c','Qs','Qh','8s','Ah','Ts']))  # queens with ace
    o = Hand(set(['3h','Qs','4s','Qh','8s','5h','Ts']))  # queens with ten
    assert h.compare(o) == 1
    assert o.compare(h) == -1

    h = Hand(set(['3d','5c','Qs','Qh','8s','2h','Ts']))  # queens with ten, eight, five
    o = Hand(set(['3d','Qs','4s','Qh','8s','5h','Ts']))  # queens with ten, eight, five
    assert h.compare(o) == 0
    assert o.compare(h) == 0

    h = Hand(set(['4s','5c','Qs','Qh','8s','2h','Ts']))  # queens with ten, eight, five
    o = Hand(set(['4s','Qs','6s','Qh','8s','5h','Ts']))  # queens with ten, eight, six
    assert h.compare(o) == -1

    h = Hand(set(['3d','5c','Qs','Qh','8s','2d','Tc']))  # queens with ten, eight, five
    o = Hand(set(['3d','5c','2s','2h','8s','2d','Tc']))  # three deuces
    assert h.compare(o) == -1

    h = Hand(set(['3d','5d','2d','4d','Ad','6h','6s']))  # five-high straight flush
    o = Hand(set(['Ad','5d','6h','4d','8d','6d','6s']))  # ace-high flush
    assert h.compare(o) == 1

    h = Hand(set(['2h','3c','4d','7h','8s','9h','Tc']))  # ten high
    o = Hand(set(['2h','3c','4d','7d','8s','9h','Ts']))  # ten high
    assert h.compare(o) == 0

    h = Hand(set(['2h','3c','4d','7h','8s','9h','6c']))  # nine high
    o = Hand(set(['2h','3c','4d','7d','8s','9h','Ts']))  # ten high
    assert h.compare(o) == -1

    h = Hand(set(['3d','4c','2s','3h','4s','2h','2c']))  # deuces full of fours
    o = Hand(set(['3d','Ac','2s','3h','4s','As','2c']))  # aces and treys
    assert h.compare(o) == 1

    h = Hand(set(['3d','Ac','Js','3h','4s','As','2c']))  # aces and treys, jack kicker
    o = Hand(set(['3d','Ac','9s','3h','4s','As','2h']))  # aces and treys, nine kicker
    assert h.compare(o) == 1

    h = Hand(set(['3d','Ac','Js','3h','4s','As','2c']))  # aces and treys, jack kicker
    o = Hand(set(['3d','Ac','Js','3s','4s','As','2h']))  # aces and treys, jack kicker
    assert h.compare(o) == 0

    h = Hand(set(['3d','5d','2s','5c','As','5h','5s']))  # four fives, ace kicker
    o = Hand(set(['Ad','5d','3s','5c','As','5h','5s']))  # four fives, ace kicker
    assert h.compare(o) == 0

    h = Hand(set(['3d','5d','2s','5c','As','5h','5s']))  # four fives, ace kicker
    o = Hand(set(['3d','5d','Ts','5c','Qs','5h','5s']))  # four fives, queen kicker
    assert h.compare(o) == 1

    h = Hand(set(['3d','4c','6s','7h','Ks','5h','Tc']))  # straight to the seven
    o = Hand(set(['8d','9c','6s','7h','Ks','5h','Tc']))  # straight to the ten
    assert h.compare(o) == -1

    h = Hand(set(['Ad','5d','Td','Jd','Kd','Qd','6h']))  # royal flush
    o = Hand(set(['9d','5d','Td','Jd','Kd','Qd','6d']))  # king-high straight flush
    assert h.compare(o) == 1

    h = Hand(set(['Kh','5s','4s','6s','8s','7h','9s']))  # nine-high flush with nine-high straight
    o = Hand(set(['Kh','5s','Th','6s','8s','7h','9h']))  # ten-high straight
    assert h.compare(o) == 1


def test_shuffle_and_draw():
    reshuffle()
    for _ in range(52):
        draw_card()
    with pytest.raises(StopIteration):
        draw_card()
    reshuffle()
    for _ in range(26):
        draw_card()
    reshuffle()
    cards = set()
    for _ in range(26):
        cards |= set([draw_card()])
    print(cards)
    assert len(cards) == 26
    for _ in range(26):
        cards |= set([draw_card()])
    assert len(cards) == 52
    reshuffle()
    for _ in range(32):
        draw_card()
    for _ in range(20):
        draw_card()
    with pytest.raises(StopIteration):
        draw_card()


def test_card_names():
    assert card_name('As') == 'ace of spades'
    assert card_name('2h') == 'deuce of hearts'
    assert card_name('3d') == 'trey of diamonds'
    assert card_name('4d') == 'four of diamonds'
    assert card_name('5c') == 'five of clubs'
    assert card_name('6c') == 'six of clubs'
    assert card_name('7c') == 'seven of clubs'
    assert card_name('8d') == 'eight of diamonds'
    assert card_name('9d') == 'nine of diamonds'
    assert card_name('Th') == 'ten of hearts'
    assert card_name('Jh') == 'jack of hearts'
    assert card_name('Qs') == 'queen of spades'
    assert card_name('Ks') == 'king of spades'
    with pytest.raises(AssertionError):
        card_name(None)
    with pytest.raises(AssertionError):
        card_name('A')
    with pytest.raises(AssertionError):
        card_name('A5s')
    with pytest.raises(AssertionError):
        card_name('Ax')
    with pytest.raises(AssertionError):
        card_name('1s')
    with pytest.raises(AssertionError):
        card_name('h3')
    with pytest.raises(AssertionError):
        card_name(['A','s'])
    with pytest.raises(AssertionError):
        card_name({'2h'})


def test_game_players_cycle():
    game = Game(n=5)
    assert len(game.players) == 5
    assert game.active_players == 5
    assert game.players[0].button
    assert game.dealer == game.players[0]
    for player in game.players[1:]:
        assert not player.button

    current_player = game.players[0]
    current_player = current_player.next
    current_player = current_player.next
    current_player = current_player.next
    assert current_player == game.players[3]
    current_player = current_player.next
    current_player = current_player.next
    assert game.active_players == 5
    assert current_player == game.players[0]
    for _ in range(57):  # 11 full cycles + 2 positions
        current_player = current_player.next
    assert current_player == game.players[2]
    current_player = current_player.next
    game.remove_player(2)
    assert game.active_players == 4
    assert current_player == game.players[3]
    current_player = current_player.next
    current_player = current_player.next
    current_player = current_player.next
    assert current_player == game.players[1]
    current_player = current_player.next
    assert current_player == game.players[3]
    with pytest.raises(AssertionError):
        game.remove_player(2)
    assert game.active_players == 4
    current_player = current_player.next
    assert current_player == game.players[4]
    game.remove_player(0)
    assert game.active_players == 3
    current_player = current_player.next
    assert current_player == game.players[1]
    for _ in range(57):  # 3 players left, 57 is divisible by 3
        current_player = current_player.next
    assert current_player == game.players[1]
    current_player = current_player.next
    assert current_player == game.players[3]
    game.remove_player(1)
    assert game.active_players == 2
    current_player = current_player.next
    assert current_player == game.players[4]
    current_player = current_player.next
    assert current_player == game.players[3]
    current_player = current_player.next
    assert current_player == game.players[4]
    assert current_player.prev == current_player.next


# TODO: create game n=2, fold at each stage and check board and deck are correctly allocated
def test_headsup_game_variable_allocation(monkeypatch):
    pass


# TODO: modify a game to use and award side pots
def test_side_action():
    pass
