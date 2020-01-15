from main import Board, Game
from players import Player
from errors import ModeNotExist
import pytest


def test_basic_board():
    board = Board()

    assert board.get_pawn((2, 2)) == 3
    for col in range(5):
        assert board.get_pawn((0, col)) == 2
        assert board.get_pawn((4, col)) == 1
        assert board.get_pawn((3, col)) == 0


def test_move():
    board = Board()

    assert board.get_pawn((4, 0)) == 1
    assert board.get_pawn((1, 0)) == 0

    board.replace((4, 0), (1, 0))

    assert board.get_pawn((4, 0)) == 0
    assert board.get_pawn((1, 0)) == 1


def test_possible_pawns():
    board = Board()
    player = Player(1)

    assert board.get_possible_pawns(player) == [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]


def test_max_directed_path():
    board = Board()

    assert board.get_max_directed_path((4, 0), (-1, 0)) == (1, 0)
    assert board.get_max_directed_path((4, 2), (-1, 1)) == (2, 4)


def test_all_max_paths():
    board = Board()

    assert board.get_all_max_paths((4, 2)) == sorted([(2, 0), (3, 2), (2, 4)])


# Game
def test_mode():
    with pytest.raises(ModeNotExist):
        game = Game(video_mode=10)

    with pytest.raises(ModeNotExist):
        game = Game(video_mode=1, game_mode=10)


def test_game_ends():
    game = Game(video_mode=1, game_mode=4)
    game.play()
