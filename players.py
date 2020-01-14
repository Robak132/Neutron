from random import choice
from errors import WrongPawn, WrongData, WrongCoordinates, WrongTarget, BlockedPawn


class Player:
    """
    Main class describing player in the game.
    """
    def get_id(self):
        return self.id

    def is_bot(self):
        return self.bot

    def move_pawn(self, origin_coordinates, target_coordinates, board):
        board.replace(origin_coordinates, target_coordinates)


class HumanPlayer(Player):
    """
    Main class describing human player in the game.
    """
    def __init__(self, id):
        self.id = id
        self.bot = False

    def get_selected_pawn(self, board, interface):
        pawn = None
        while pawn is None:
            try:
                return interface.select_pawn(self)
            except WrongData:
                interface.print_error("You gave wrong data or used wrong format. Try again.")
            except WrongCoordinates:
                interface.print_error("You gave wrong coordinates. Try again.")
            except WrongPawn:
                interface.print_error("You selected wrong pawn. Try again.")
            except BlockedPawn:
                interface.print_error("You selected pawn that is fully blocked. Try again.")
            except KeyboardInterrupt:
                raise SystemExit
            except EOFError:
                raise SystemExit

    def get_selected_target(self, pawn, board, interface):
        target = None
        while target is None:
            try:
                return interface.select_target(pawn)
            except WrongData:
                interface.print_error("You gave wrong data or used wrong format. Try again.")
            except WrongCoordinates:
                interface.print_error("You gave wrong coordinates. Try again.")
            except WrongTarget:
                interface.print_error("You selected wrong target. Try again.")
            except KeyboardInterrupt:
                raise SystemExit
            except EOFError:
                raise SystemExit


class RandomBot(Player):
    """
    Main class describing easy bot in the game. It always takes random valid move.
    """
    def __init__(self, id):
        self.id = id
        self.bot = True

    def get_selected_pawn(self, board, interface):
        return choice(board.get_possible_pawns(self))

    def get_selected_target(self, pawn, board, inteface):
        return choice(board.get_all_max_paths(pawn))


class SmartBot(Player):
    def __init__(self, id):
        self.id = id
        self.bot = True

    def get_selected_pawn(self, board, interface):
        if self.get_id() == 1:
            enemy_row = 0
            home_row = 4
        else:
            enemy_row = 4
            home_row = 0

        possible_pawns = board.get_possible_pawns(self)
        primary_pawns = []
        for pawn in possible_pawns:
            for row, column in board.get_all_max_paths(pawn):
                if row == enemy_row and pawn not in primary_pawns:
                    primary_pawns.append(pawn)

        # secondary_pawns = [pawn for pawn in possible_pawns if pawn in board.get_all_max_paths(board.get_neutron())]
        secondary_pawns = []

        if primary_pawns != []:
            return choice(primary_pawns)
        elif secondary_pawns != []:
            return choice(secondary_pawns)
        else:
            return choice(possible_pawns)

    def get_selected_target(self, pawn, board, teminal):
        possible_targets = board.get_all_max_paths(pawn)
        if self.get_id() == 1:
            enemy_row = 0
            home_row = 4
        else:
            enemy_row = 4
            home_row = 0

        if pawn == board.get_neutron():
            primary_targets = [(row, column) for (row, column) in possible_targets if row == home_row]
            secondary_targets = [(row, column) for (row, column) in possible_targets if row != enemy_row]
            tertiary_targets = [(row, column) for (row, column) in possible_targets if (enemy_row, 0) not in board.get_all_max_paths(pawn) if (enemy_row, 1) not in board.get_all_max_paths(pawn) if (enemy_row, 2) not in board.get_all_max_paths(pawn) if (enemy_row, 3) not in board.get_all_max_paths(pawn) if (enemy_row, 4) not in board.get_all_max_paths(pawn)]
        else:
            primary_targets = [(row, column) for (row, column) in possible_targets if row == enemy_row]
            secondary_targets = []
            tertiary_targets = []

        if primary_targets != []:
            return choice(primary_targets)
        elif secondary_targets != []:
            return choice(secondary_targets)
        elif tertiary_targets != []:
            return tertiary_targets
        else:
            return choice(possible_targets)
