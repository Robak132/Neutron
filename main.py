from random import choice
from errors import InvalidAction, SelectedWrongPawn


class Board:
    """
    Main class describing gameboard.
    """
    def __init__(self, custom=None):
        """
        :custom list of lists: sets custom board for game.
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

    def move(self, origin_coordinates, target_coordinates):
        origin_row, origin_column = origin_coordinates
        target_row, target_column = target_coordinates

        _temp = self.board[target_row][target_column]
        self.board[target_row][target_column] = self.board[origin_row][origin_column]
        self.board[origin_row][origin_column] = _temp

    def get_pawns_by_id(self, id):
        """
        Returns coordinates of all pawns with given id.
        :param id int: id of pawns you are searching for
        """
        coordinates = []
        for row in range(0, len(self.board)):
            for column in range(0, len(self.board[row])):
                if self.board[row][column] == id:
                    coordinates.append((row, column))
        return coordinates

    def get_pawn(self, coordinates):
        row, column = coordinates

        return self.board[row][column]

    def get_all_max_paths(self, origin_coordinates):
        paths = []
        for vector in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
            if self.get_max_directed_path((origin_coordinates), vector) != origin_coordinates:
                if self.get_max_directed_path((origin_coordinates), vector) not in paths:
                    paths.append(self.get_max_directed_path((origin_coordinates), vector))
        return paths

    def print_all_max_paths(self, origin_coordinates):
        print(f"Possible targets:\n{self.get_all_max_paths(origin_coordinates)}")

    def get_max_directed_path(self, origin_coordinates, vector):
        vector_y, vector_x = vector
        origin_y, origin_x = origin_coordinates

        if (origin_x + vector_x < 0 or origin_x + vector_x > 4) or (origin_y + vector_y < 0 or origin_y + vector_y > 4):
            return origin_coordinates
        if self.board[origin_y + vector_y][origin_x + vector_x] != 0:
            return origin_coordinates
        else:
            return self.get_max_directed_path((origin_y + vector_y, origin_x + vector_x), vector)

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

    def print_possible_pawns(self, board):
        print(f"Possible pawns:")
        for pawn in self.get_possible_pawns(board)[:-1]:
            print(f"{pawn}, ", end="")
        print(f"{pawn}")  

    def move_pawn(self, origin_coordinates, target_coordinates, board):
        if board.get_pawn(origin_coordinates) == self.id:
            board.move(origin_coordinates, target_coordinates)
        else:
            raise SelectedWrongPawn

    def move_neutron(self, origin_coordinates, target_coordinates, board):
        if board.get_pawn(origin_coordinates) == 3:
            board.move(origin_coordinates, target_coordinates)
        else:
            raise SelectedWrongPawn

    def __str__(self):
        return f"Player {self.id}"


class Game:
    def play_2_humans(self, board):
        players = [Player(1), Player(2)]
        active_player = choice(players)
        while True:
            print(active_player)
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
