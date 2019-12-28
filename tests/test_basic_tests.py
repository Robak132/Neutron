from main import Board, Player, Game


def test_basic_test_1():
    board = Board()

    assert board.get_pawn((2, 2)) == 3
    for col in range(5):
        assert board.get_pawn((0, col)) == 2
        assert board.get_pawn((4, col)) == 1
        assert board.get_pawn((3, col)) == 0
