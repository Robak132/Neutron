from main import Game, Board, Player


def test_player_1_wins():
    test_board = [
        [2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [3, 1, 1, 1, 1]
    ]
    game = Game([Player(1), Player(2)], board=Board(custom=test_board), first_turn=False)
    assert game.get_winner() == 1


def test_player_2_wins():
    test_board = [
        [2, 2, 3, 2, 2],
        [0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1]
    ]
    game = Game([Player(1), Player(2)], board=Board(custom=test_board), first_turn=False)
    assert game.get_winner() == 2


def test_draw_wins():
    test_board = [
        [2, 2, 0, 0, 0],
        [2, 2, 0, 0, 0],
        [3, 2, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0]
    ]
    game = Game([Player(1), Player(2)], board=Board(custom=test_board), first_turn=False)
    assert game.get_winner() == 3
