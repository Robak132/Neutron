from main import Board
from players import Player
from interfaces import TextInterface
from errors import WrongCoordinates, WrongData, WrongPawn, WrongTarget, BlockedPawn
import pytest


def test_select_pawn_1():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)
    player = Player(1)

    with pytest.raises(WrongData):
        interface.select_pawn(player, test="3,5,6")


def test_select_pawn_2():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)
    player = Player(1)

    with pytest.raises(WrongData):
        interface.select_pawn(player, test="35")


def test_select_pawn_3():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)
    player = Player(1)

    with pytest.raises(WrongCoordinates):
        interface.select_pawn(player, test="10,10")


def test_select_pawn_4():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)
    player = Player(1)

    with pytest.raises(WrongPawn):
        interface.select_pawn(player, test="0,0")  # Player 1 tries to move player 2 pawn


def test_select_pawn_5():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)
    player = Player(1)

    with pytest.raises(BlockedPawn):
        interface.select_pawn(player, test="4,4")


def test_select_target_1():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)

    with pytest.raises(WrongData):
        interface.select_target((4, 0), test="3,5,6")


def test_select_target_2():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)

    with pytest.raises(WrongData):
        interface.select_target((4, 0), test="3")


def test_select_target_3():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)

    with pytest.raises(WrongCoordinates):
        interface.select_target((4, 0), test="10,10")


def test_select_target_4():
    board = Board(custom=[
        [2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 2],
        [1, 1, 1, 1, 1],
    ])
    interface = TextInterface(board)

    with pytest.raises(WrongTarget):
        interface.select_target((4, 0), test="3,2")
