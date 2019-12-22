from random import choice
from errors import InvalidAction, SelectedWrongPawn


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

    def get_all_max_paths(self, origin_coordinates):
        _paths = []
        for vector in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
            if self.get_max_directed_path((origin_coordinates), vector) != origin_coordinates:
                if self.get_max_directed_path((origin_coordinates), vector) not in _paths:
                    _paths.append(self.get_max_directed_path((origin_coordinates), vector))
        return _paths

    def get_max_directed_path(self, origin_coordinates, vector):
        vector_y, vector_x = vector
        origin_y, origin_x = origin_coordinates

        if (origin_x + vector_x < 0 or origin_x + vector_x > 4) or (origin_y + vector_y < 0 or origin_y + vector_y > 4):
            return origin_coordinates
        if self.board[origin_y + vector_y][origin_x + vector_x] != 0:
            return origin_coordinates
        else:
            return self.get_max_directed_path((origin_y + vector_y, origin_x + vector_x), vector)

    def print_all_max_paths(self, origin_coordinates):
        print(f"Possible targets:\n{self.get_all_max_paths(origin_coordinates)}")

    def print_board(self):
        print(f"  ", end="")
        for col in range(5):
            print(f" \033[93m{col}\033[0m ", end="")
        print()

        for row in range(5):
            print(f"\033[93m{row}\033[0m ", end="")
            for col in range(5):
                print(f" {self.board[row][col]} ", end="")
            print()
        print()


class Player:
    """
    Main class describing player/bot in the game.
    """
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def get_possible_pawns(self, board):
        _pawns = []
        for _pawn in board.get_pawns_by_id(self.id):
            if board.get_all_max_paths(_pawn) != []:
                _pawns.append(_pawn)
        return _pawns

    def move_pawn(self, origin_coordinates, target_coordinates, board):
        if board.get_pawn(origin_coordinates) == self.id:
            board.replace(origin_coordinates, target_coordinates)
        else:
            raise SelectedWrongPawn

    def move_neutron(self, target_coordinates, board):
        origin_coordinates = board.get_pawns_by_id(3)[0]
        board.replace(origin_coordinates, target_coordinates)

    def print_possible_pawns(self, board):
        print(f"Possible pawns:")
        for pawn in self.get_possible_pawns(board)[:-1]:
            print(f"{pawn}, ", end="")
        print(f"{self.get_possible_pawns(board)[-1]}")

    def __str__(self):
        return f"Player {self.id}"


class Game:
    def play_2_humans(self, board):
        players = [Player(1), Player(2)]
        active_player = choice(players)
        first_turn = True
        while True:
            print(active_player)

            if not first_turn:
                board.print_board()
                board.print_all_max_paths(board.get_pawns_by_id(3)[0])
                _target = input("Choose target for neutron:\n")
                _target = _target.split(", ")
                target = [int(coordinate) for coordinate in _target]
                target = tuple(target)
                active_player.move_neutron(target, board)
            else:
                first_turn = False

            board.print_board()
            active_player.print_possible_pawns(board)
            _pawn = input("Choose pawn:\n")
            _pawn = _pawn.split(", ")
            pawn = [int(coordinate) for coordinate in _pawn]
            pawn = tuple(pawn)

            board.print_all_max_paths(pawn)
            _target = input("Choose target:\n")
            _target = _target.split(", ")
            target = [int(coordinate) for coordinate in _target]
            target = tuple(target)
            active_player.move_pawn(pawn, target, board)

            if players.index(active_player) == 0:
                active_player = players[1]
            else:
                active_player = players[0]


if __name__ == "__main__":
    board = Board()
    game = Game()
    game.play_2_humans(board)
