from main import Board
from players import RandomBot, SmartBot
from interfaces import TextInterface


def test_random_bot():
    bot = RandomBot(1)
    board = Board(custom=[
        [2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1]
    ])
    assert bot.get_selected_pawn(board, TextInterface(board)) in [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    assert bot.get_selected_target((4, 0), board, TextInterface(board)) in [(1, 0), (3, 1)]


def test_smart_bot_1():
    bot1 = SmartBot(1)
    board = Board(custom=[
        [0, 2, 2, 2, 2],
        [0, 0, 2, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1]
    ])
    assert bot1.get_selected_pawn(board, TextInterface(board)) == (4, 0)
    assert bot1.get_selected_target((4, 0), board, TextInterface(board)) == (0, 0)
    assert bot1.get_selected_target((4, 0), board, TextInterface(board)) != (3, 1)


def test_smart_bot_2():
    bot2 = SmartBot(2)
    board = Board(custom=[
        [0, 2, 2, 2, 2],
        [0, 0, 2, 0, 0],
        [0, 0, 3, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1]
    ])
    assert bot2.get_selected_target((2, 2), board, TextInterface(board)) == (0, 0)
    board = Board(custom=[
        [2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1]
    ])
    assert bot2.get_selected_target((2, 2), board, TextInterface(board)) != (4, 2)
