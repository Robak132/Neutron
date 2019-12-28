from main import Game, Board, Player


def test_player_1_wins():
    test_board = [
        [2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [3, 1, 1, 1, 1]
    ]
    game = Game(video_mode=0)
    game.players = [Player(0), Player(1)]
    game.board = Board(custom=test_board)
    assert game.get_winner() == 1


def test_player_2_wins():
    test_board = [
        [2, 2, 3, 2, 2],
        [0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1]
    ]
    game = Game(video_mode=0)
    game.players = [Player(0), Player(1)]
    game.board = Board(custom=test_board)
    assert game.get_winner() == 2


def test_draw_wins():
    test_board = [
        [2, 2, 0, 0, 0],
        [2, 2, 0, 0, 0],
        [3, 2, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0]
    ]
    game = Game(video_mode=0)
    game.players = [Player(0), Player(1)]
    game.board = Board(custom=test_board)
    assert game.get_winner() == 3
