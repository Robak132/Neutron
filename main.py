from random import choice
from errors import WrongPawn, WrongData, WrongCoordinates, WrongTarget
from sys import exit
import os
from colorama import init as colorinit


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

    def get_pawn(self, coordinates):
        """
        Returns id of the element with given coordiantes.
        :param coordinates tuple of ints: coordinates of element
        """
        _row, _column = coordinates

        return self.board[_row][_column]

    def get_neutron(self):
        return self.get_pawns_by_id(3)[0]

    def get_all_max_paths(self, origin_coordinates):
        _paths = []
        for vector in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
            if self.get_max_directed_path((origin_coordinates), vector) != origin_coordinates:
                if self.get_max_directed_path((origin_coordinates), vector) not in _paths:
                    _paths.append(self.get_max_directed_path((origin_coordinates), vector))
        return sorted(_paths)

    def get_max_directed_path(self, origin_coordinates, vector):
        vector_row, vector_column = vector
        origin_row, origin_column = origin_coordinates

        if not self.validate_coordinates((origin_row + vector_row, origin_column + vector_column)):
            return origin_coordinates
        if self.get_pawn((origin_row + vector_row, origin_column + vector_column)) != 0:
            return origin_coordinates
        else:
            return self.get_max_directed_path((origin_row + vector_row, origin_column + vector_column), vector)

    def print_all_max_paths(self, origin_coordinates):
        print(f"Possible targets:")
        for path in self.get_all_max_paths(origin_coordinates)[:-1]:
            print(f"{path}, ", end="")
        print(f"{self.get_all_max_paths(origin_coordinates)[-1]}")

    def print_board(self):
        print(f"  ", end="")
        for col in range(5):
            print(f" \033[93m{col}\033[0m ", end="")
        print()

        for row in range(5):
            print(f"\033[93m{row}\033[0m ", end="")
            for col in range(5):
                if self.get_pawn((row, col)) == 1:
                    print(f" \033[92m{self.board[row][col]}\033[0m ", end="")
                elif self.get_pawn((row, col)) == 2:
                    print(f" \033[91m{self.board[row][col]}\033[0m ", end="")
                elif self.get_pawn((row, col)) == 3:
                    print(f" \033[94m{self.board[row][col]}\033[0m ", end="")
                else:
                    print(f" {self.board[row][col]} ", end="")
            print()
        print()


class Player:
    """
    Main class describing player in the game.
    """
    def __init__(self, id):
        self.id = id
        self.bot = False

    def get_id(self):
        return self.id

    def is_bot(self):
        return self.bot

    def get_possible_pawns(self, board):
        _pawns = []
        for _pawn in board.get_pawns_by_id(self.id):
            if board.get_all_max_paths(_pawn) != []:
                _pawns.append(_pawn)
        return sorted(_pawns)

    def get_selected_pawn(self, board):
        _pawn = input("Select pawn (row, column):\n").replace(" ", "")
        _pawn = _pawn.split(",")

        # Not 2 coordinates
        if len(_pawn) != 2:
            raise WrongData

        # Value not int
        _coordinates = []
        for _coordinate in _pawn:
            try:
                _coordinates.append(int(_coordinate))
            except ValueError:
                raise WrongData

        # Coordinates not on board
        if not board.validate_coordinates(tuple(_coordinates)):
            raise WrongCoordinates

        # Not valid pawn
        if board.get_pawn(_coordinates) != self.get_id():
            raise WrongPawn

        return tuple(_coordinates)

    def get_selected_target(self, pawn, board):
        _target = input("Select target (row, column):\n").replace(" ", "")
        _target = _target.split(",")

        # Not 2 coordinates
        if len(_target) != 2:
            raise WrongData

        # Value not int
        _coordinates = []
        for _coordinate in _target:
            try:
                _coordinates.append(int(_coordinate))
            except ValueError:
                raise WrongData

        # Coordinates not on board
        if not board.validate_coordinates(tuple(_coordinates)):
            raise WrongCoordinates

        # Not valid target
        if tuple(_coordinates) not in board.get_all_max_paths(pawn):
            raise WrongTarget

        return tuple(_coordinates)

    def move_pawn(self, origin_coordinates, target_coordinates, board):
        board.replace(origin_coordinates, target_coordinates)

    def print_possible_pawns(self, board):
        print(f"Possible pawns:")
        for pawn in self.get_possible_pawns(board)[:-1]:
            print(f"{pawn}, ", end="")
        print(f"{self.get_possible_pawns(board)[-1]}")

    def __str__(self):
        return f"Player {self.id}"


class RandomBot(Player):
    """
    Main class describing easy bot in the game. It always takes random valid move.
    """
    def __init__(self, id):
        self.id = id
        self.bot = True

    def get_selected_pawn(self, board):
        return choice(self.get_possible_pawns(board))

    def get_selected_target(self, pawn, board):
        return choice(board.get_all_max_paths(pawn))


class SmartBot(Player):
    def __init__(self, id):
        self.id = id
        self.bot = True

    def get_selected_pawn(self, board):
        if self.get_id() == 1:
            enemy_row = 0
            player_row = 4
        else:
            enemy_row = 4
            player_row = 0

        possible_pawns = self.get_possible_pawns(board)
        priority_pawns = []
        for pawn in possible_pawns:
            for row, column in board.get_all_max_paths(pawn):
                if row == enemy_row and pawn not in priority_pawns:
                    priority_pawns.append(pawn)

        # secondary_pawns = [pawn for pawn in possible_pawns if pawn in board.get_all_max_paths(board.get_neutron())]
        secondary_pawns = []

        if priority_pawns != []:
            return choice(priority_pawns)
        elif secondary_pawns != []:
            return choice(secondary_pawns)
        else:
            return choice(possible_pawns)

    def get_selected_target(self, pawn, board):
        possible_targets = board.get_all_max_paths(pawn)
        if self.get_id() == 1:
            enemy_row = 0
            player_row = 4
        else:
            enemy_row = 4
            player_row = 0

        if pawn == board.get_neutron():
            priority_targets = [(row, column) for (row, column) in possible_targets if row == player_row]
            secondary_targets = [(row, column) for (row, column) in possible_targets if row != enemy_row]
            third_targets = [(row, column) for (row, column) in possible_targets if (enemy_row, 0) not in board.get_all_max_paths(pawn) if (enemy_row, 1) not in board.get_all_max_paths(pawn) if (enemy_row, 2) not in board.get_all_max_paths(pawn) if (enemy_row, 3) not in board.get_all_max_paths(pawn) if (enemy_row, 4) not in board.get_all_max_paths(pawn)]
        else:
            priority_targets = [(row, column) for (row, column) in possible_targets if row == enemy_row]
            secondary_targets = []
            third_targets = []

        if priority_targets != []:
            return choice(priority_targets)
        elif secondary_targets != []:
            return choice(secondary_targets)
        elif third_targets != []:
            return third_targets
        else:
            return choice(possible_targets)


class Game:
    def __init__(self, players, board=None, first_turn=None):
        if board is not None:
            self.board = board
        else:
            self.board = Board()

        if first_turn is not None:
            self.first_turn = first_turn
        else:
            self.first_turn = True

        self.players = players

        self.show_results = False
        for player in self.players:
            if not player.is_bot():
                self.show_results = True

    def select_pawn(self):
        pawn = None
        while pawn is None:
            try:
                return self.active_player.get_selected_pawn(self.board)
            except WrongData:
                print(f"\033[91m{'You gave wrong data or used wrong format. Try again.'}\033[0m")
            except WrongCoordinates:
                print(f"\033[91m{'You gave wrong coordinates. Try again.'}\033[0m")
            except WrongPawn:
                print(f"\033[91m{'You selected wrong pawn. Try again.'}\033[0m")
            except KeyboardInterrupt:
                exit()

    def select_target(self, pawn):
        target = None
        while target is None:
            try:
                return self.active_player.get_selected_target(pawn, self.board)
            except WrongData:
                print(f"\033[91m{'You gave wrong data or used wrong format. Try again.'}\033[0m")
            except WrongCoordinates:
                print(f"\033[91m{'You gave wrong coordinates. Try again.'}\033[0m")
            except WrongTarget:
                print(f"\033[91m{'You selected wrong target. Try again.'}\033[0m")
            except KeyboardInterrupt:
                exit()

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

    def print_winner(self, board):
        board.print_board()
        if self.get_winner() == 1:
            print("\033[33mPlayer 1 wins\033[0m")
        elif self.get_winner() == 2:
            print("\033[33mPlayer 2 wins\033[0m")
        elif self.get_winner() == 3:
            print("\033[33mDraw\033[0m")
        input("Press Enter to exit...")

    def play(self):
        # Initialization
        self.active_player = choice(self.players)

        while self.get_winner() is None:
            # Beginning of turn
            os.system("cls")

            # Neutron turn
            if not self.first_turn:
                neutron = self.board.get_neutron()
                if not self.active_player.is_bot():
                    print(f"\033[93mNeutron's Turn\033[0m\n")
                    self.board.print_board()
                    self.board.print_all_max_paths(neutron)
                target = self.select_target(neutron)
                self.active_player.move_pawn(neutron, target, self.board)
            else:
                self.first_turn = False

            # Check for win
            if self.get_winner() is not None:
                if self.show_results:
                    self.print_winner(self.board)
                return self.get_winner()

            # Selecting pawn
            if not self.active_player.is_bot():
                print(f"\033[93mPlayer's {self.active_player.get_id()} Turn\033[0m\n")
                self.board.print_board()
                self.active_player.print_possible_pawns(self.board)
            pawn = self.select_pawn()

            # Selecting pawn's target
            if not self.active_player.is_bot():
                self.board.print_all_max_paths(pawn)
            target = self.select_target(pawn)

            # Moving pawns
            self.active_player.move_pawn(pawn, target, self.board)

            # Ending turn
            if self.players.index(self.active_player) == 0:
                self.active_player = self.players[1]
            else:
                self.active_player = self.players[0]

        if self.show_results:
            self.print_winner(self.board)
        return self.get_winner()


if __name__ == "__main__":
    colorinit()
    while True:
        try:
            print("\033[93mChoose game mode:\n1: One player mode with easy computer\n2: One player mode with hard computer\n3: Two players mode\n4: Debug mode\033[0m")
            mode = input()
        except KeyboardInterrupt:
            exit()

        if mode == "1":
            game = Game([Player(1), RandomBot(2)])
            game.play()
            break
        elif mode == "2":
            game = Game([Player(1), SmartBot(2)])
            game.play()
            break
        elif mode == "3":
            game = Game([Player(1), Player(2)])
            game.play()
            break
        elif mode == "4":
            games = input("Give number of games:\n")
            results = {
                1: 0,
                2: 0,
                3: 0
            }
            for g in range(int(games)):
                game = Game([RandomBot(1), SmartBot(2)])
                result = game.play()
                results[result] += 1
            print(f"Game results:\nWin by 1: {results[1]}\nWin by 2: {results[2]}\nDraws: {results[3]}")
            input("Press Enter to exit...")
        else:
            print("Invalid input. Try again.")
            mode = ""
