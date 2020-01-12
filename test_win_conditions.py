from main import Game, Board
from interfaces import TextInterface, GUI
from players import HumanPlayer, RandomBot, SmartBot

from random import choice
from sys import exit
from colorama import init as colorinit
from os import system


def test_player_1_wins():
    test_board = [
        [2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [3, 1, 1, 1, 1]
    ]
    game = Game(video_mode=1,game_mode=2)
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
    game = Game(video_mode=1,game_mode=4)
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
    game = Game(video_mode=1,game_mode=4)
    game.board = Board(custom=test_board)
    assert game.get_winner() == 3
