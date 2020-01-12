from interfaces import TextInterface, GUI
from players import HumanPlayer, RandomBot, SmartBot

from random import choice
from colorama import init as colorinit
from os import system
import pygame


# Board
class Board:
    """
    Main class describing gameboard.
    """
    def __init__(self, custom=None):
        """
            :param list of lists custom: sets custom board for game.
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
            :param tuple of ints origin_coordinates: Coordinates of first element
            :param tuple of ints target_coordinates: Coordinates of second element
        """
        origin_row, origin_column = origin_coordinates
        target_row, target_column = target_coordinates

        _temp = self.board[target_row][target_column]
        self.board[target_row][target_column] = self.board[origin_row][origin_column]
        self.board[origin_row][origin_column] = _temp

    def validate_coordinates(self, coordinates):
        """
        Checks if coordinates are valid. Returns bool.
            :param tuple of ints coordinates: Given coordinates
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
            :param int id: id of pawns you are searching for
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
            :param Player player: Player that moves pawns in this moment.
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
        Returns id of the element with given coordiantes.
            :param coordinates tuple of ints: coordinates of element
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
            :param tuple of ints origin_coordinates: Coordinates of pawn.
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
            :param tuple of ints origin_coordinates: coordinates of pawn.
            :param tuple of ints vector: path vector.
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
        self.interface = self.get_video_mode(self.board, video_mode)
        self.players = self.get_game_mode(self.interface, game_mode)

        if first_turn is not None:
            self.first_turn = first_turn
        else:
            self.first_turn = True

    def get_video_mode(self, board, video_mode=None):
        if video_mode == 0:
            return GUI(board)
        else:
            return TextInterface(board)

    def get_game_mode(self, interface, game_mode=None):
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

    def get_winner(self):
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
        # Initialization
        self.active_player = choice(self.players)

        running = True
        while running:
            # Beginning of turn
            system("cls")

            # Neutron turn
            if not self.first_turn:
                neutron = self.board.get_neutron()
                if not self.active_player.is_bot():
                    self.interface.print_all(player=self.active_player, neutron=True)
                    self.interface.print_all_max_paths(neutron)
                target = self.active_player.get_selected_target(neutron, self.board, self.interface)
                self.active_player.move_pawn(neutron, target, self.board)
            else:
                self.first_turn = False

            # Check for win
            if self.get_winner() is not None:
                self.interface.print_all(winner=self.get_winner())
                pygame.time.wait(5000)
                return self.get_winner()

            # Selecting pawn
            if not self.active_player.is_bot():
                self.interface.print_all(player=self.active_player)
                self.interface.print_possible_pawns(self.active_player)
            pawn = self.active_player.get_selected_pawn(self.board, self.interface)

            # Selecting pawn's target
            if not self.active_player.is_bot():
                self.interface.print_all_max_paths(pawn)
            target = self.active_player.get_selected_target(pawn, self.board, self.interface)

            # Moving pawns
            self.active_player.move_pawn(pawn, target, self.board)

            # Ending turn
            if self.players.index(self.active_player) == 0:
                self.active_player = self.players[1]
            else:
                self.active_player = self.players[0]

            # Check for win
            if self.get_winner() is not None:
                self.interface.print_all(winner=self.get_winner())
                pygame.time.wait(5000)
                return self.get_winner()


if __name__ == "__main__":
    colorinit()
    game = Game(video_mode=0)
    game.play()
