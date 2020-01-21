from interfaces import TextInterface, GUI
from players import HumanPlayer, RandomBot, SmartBot
from errors import ModeNotExist

from random import choice
from colorama import init as colorinit
from os import system, name

import pygame
import sys


# Board
class Board:
    """
    Main class describing gameboard.
    """
    def __init__(self, custom=None):
        """
        :param custom: Custom board to replace standard board.
        :type custom: list of lists
        """
        if custom is None:
            self.reset_board()
        else:
            self.board = custom

    def reset_board(self):
        """
        Resets board to starting state.
        """
        self.board = [[0] * 5 for row in range(5)]
        self.board[0] = [2, 2, 2, 2, 2]
        self.board[2] = [0, 0, 3, 0, 0]
        self.board[4] = [1, 1, 1, 1, 1]

    def replace(self, origin_coordinates, target_coordinates):
        """
        Switches place of two elements on the board.

        :param origin_coordinates: Coordinates of first element
        :type origin_coordinates: tuple of integers

        :param target_coordinates: Coordinates of second element
        :type target_coordinates: tuple of integers

        """
        origin_row, origin_column = origin_coordinates
        target_row, target_column = target_coordinates

        self.board[target_row][target_column] = self.board[origin_row][origin_column]
        self.board[origin_row][origin_column] = 0

    def validate_coordinates(self, coordinates):
        """
        Checks if coordinates are valid. Returns bool.

        :param coordinates: Given coordinates
        :type coordinates: tuple of integers
        """
        row, column = coordinates

        if row > 4 or row < 0:
            return False
        if column > 4 or column < 0:
            return False
        return True

    def get_pawns_by_id(self, id):
        """
        Returns coordinates of all pawns with given id.

        :param id: id of pawns you are searching for
        :type id: int
        """
        coordinates = []
        for row in range(0, len(self.board)):
            for column in range(0, len(self.board[row])):
                if self.board[row][column] == id:
                    coordinates.append((row, column))
        return coordinates

    def get_possible_pawns(self, player):
        """
        Return all pawns that player can move.

        :param player: Player that moves pawns in this moment.
        :type player: Player
        """
        _pawns = []
        for _pawn in self.get_pawns_by_id(player.id):
            if self.get_all_max_paths(_pawn) != []:
                _pawns.append(_pawn)
        return sorted(_pawns)

    def get_board(self):
        """
        Returns board (list of lists).
        """
        return self.board

    def get_pawn(self, coordinates):
        """
        Returns id of the element with given coordinates.

        :param coordinates tuple of integers: coordinates of element
        :type coordinates: tuple of integers
        """
        _row, _column = coordinates

        return self.board[_row][_column]

    def get_neutron(self):
        """
        Returns coordinates of neutron.
        """
        return self.get_pawns_by_id(3)[0]

    def get_all_max_paths(self, origin_coordinates):
        """
        Returns all possible targets for pawn on given coordinates.

        :param tuple of integers origin_coordinates: Coordinates of pawn.
        :type origin_coordinates: tuple of integers
        """
        _paths = []
        for vector in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
            if self.get_max_directed_path((origin_coordinates), vector) != origin_coordinates:
                if self.get_max_directed_path((origin_coordinates), vector) not in _paths:
                    _paths.append(self.get_max_directed_path((origin_coordinates), vector))
        return sorted(_paths)

    def get_max_directed_path(self, origin_coordinates, vector):
        """
        Returns final coordinates of path along vector from given coordinates.

        :param tuple of integers origin_coordinates: coordinates of pawn.
        :type origin_coordinates: tuple of integers

        :param tuple of integers vector: path vector.
        :type vector: tuple of integers
        """
        vector_row, vector_column = vector
        origin_row, origin_column = origin_coordinates

        if not self.validate_coordinates((origin_row + vector_row, origin_column + vector_column)):
            return origin_coordinates
        if self.get_pawn((origin_row + vector_row, origin_column + vector_column)) != 0:
            return origin_coordinates
        else:
            return self.get_max_directed_path((origin_row + vector_row, origin_column + vector_column), vector)


# Game
class Game:
    def __init__(self, video_mode=None, game_mode=None, first_turn=None):
        self.board = Board()
        self.game_mode = game_mode
        self.video_mode = video_mode
        self.interface = self.set_video_mode(self.board, video_mode)
        self.players = self.set_game_mode(self.interface, game_mode)

        if first_turn is not None:
            self.first_turn = first_turn
        else:
            self.first_turn = True

    def set_video_mode(self, board, video_mode=None):
        """
        Set video mode to selected, if None sets GUI.
        """
        if int(video_mode) == 0 or video_mode is None:
            return GUI(board)
        elif int(video_mode) == 1:
            return TextInterface(board)
        else:
            raise ModeNotExist

    def set_game_mode(self, interface, game_mode=None):
        """
        Sets game mode to selected, if None runs interface.select_game_mode().
        """
        if game_mode is None:
            game_mode = interface.select_game_mode()

        if int(game_mode) == 1:
            return [HumanPlayer(1), RandomBot(2)]
        elif int(game_mode) == 2:
            return [HumanPlayer(1), SmartBot(2)]
        elif int(game_mode) == 3:
            return [HumanPlayer(1), HumanPlayer(2)]
        elif int(game_mode) == 4:
            return [SmartBot(1), SmartBot(2)]
        else:
            raise ModeNotExist

    def get_winner(self):
        """
        Returns id of the winner of the game.
        """
        neutron_row, neutron_column = self.board.get_neutron()
        if neutron_row == 0:
            return 2
        elif neutron_row == 4:
            return 1
        elif self.board.get_all_max_paths(self.board.get_neutron()) == []:
            return 3
        else:
            return None

    def play(self):
        """
        Runs game.
        """
        # Initialization
        self.active_player = choice(self.players)

        running = True
        while running:
            # Beginning of turn
            system('cls' if name == 'nt' else 'clear')  # Win vs Linux

            # Neutron turn
            if not self.first_turn:
                neutron = self.board.get_neutron()
                if not self.active_player.is_bot():
                    self.interface.print_header(f"Neutron's Turn (Player {self.active_player.get_id()})")
                    self.interface.print_all_max_paths(neutron)
                target = self.active_player.get_selected_target(neutron, self.board, self.interface)
                self.active_player.move_pawn(neutron, target, self.board)
            else:
                self.first_turn = False

            # Check for win
            if self.get_winner() is not None:
                self.interface.print_winner(self.get_winner())
                pygame.time.wait(1000)
                if self.game_mode != 4:
                    return self.interface.select_game_end(self.get_winner())
                else:
                    return self.get_winner()

            # Selecting pawn
            if not self.active_player.is_bot():
                self.interface.print_header(f"Player's {self.active_player.get_id()} Turn")
                self.interface.print_possible_pawns(self.active_player)
            pawn = self.active_player.get_selected_pawn(self.board, self.interface)

            # Selecting pawn's target
            if not self.active_player.is_bot():
                self.interface.print_all_max_paths(pawn)
            target = self.active_player.get_selected_target(pawn, self.board, self.interface)

            # Moving pawns
            self.active_player.move_pawn(pawn, target, self.board)

            # Check for win
            if self.get_winner() is not None:
                self.interface.print_winner(self.get_winner())
                pygame.time.wait(1000)
                if self.game_mode != 4:
                    return self.interface.select_game_end(self.get_winner())
                else:
                    return self.get_winner()
            # Ending turn
            if self.players.index(self.active_player) == 0:
                self.active_player = self.players[1]
            else:
                self.active_player = self.players[0]


if __name__ == "__main__":
    colorinit()
    print(sys.argv)
    try:
        if len(sys.argv) == 1:
            game = Game(video_mode=0)
        elif len(sys.argv) == 2:
            game = Game(video_mode=sys.argv[1])
        elif len(sys.argv) == 3:
            game = Game(video_mode=sys.argv[1], game_mode=sys.argv[2])
    except ModeNotExist:
        sys.exit("Mode don't exist")

    running = True
    while running:
        result = game.play()
        if result is None:
            running = False
        else:
            game.set_game_mode(game.interface)
            game.play()
