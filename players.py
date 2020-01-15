from random import choice
from errors import WrongPawn, WrongData, WrongCoordinates, WrongTarget, BlockedPawn


class Player:
    """
    Main class describing player in the game.
    :params id: ID of the Player (Position on board 1-Bottom, 2-Top).
    """
    def __init__(self, id):
        self.id = id
        self.bot = True

    def get_id(self):
        return self.id

    def is_bot(self):
        return self.bot

    def move_pawn(self, origin_coordinates, target_coordinates, board):
        """
        Moves pawn on the board using board.replace().
        """
        board.replace(origin_coordinates, target_coordinates)


class HumanPlayer(Player):
    """
    Main class describing human player in the game.
    """
    def __init__(self, id):
        self.id = id
        self.bot = False

    def get_selected_pawn(self, board, interface):
        """
        Runs interface.select_pawn(), catches Exceptions and prints them using interface. 
        Returns coordinates of the target.
        """
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
        """
        Runs interface.select_target(), catches Exceptions and prints them using interface. 
        Returns coordinates of the target.
        """
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
    Main class describing easy bot in the game.
    It always takes random valid move.
    """
    def __init__(self, id):
        self.id = id
        self.bot = True

    def get_selected_pawn(self, board, interface):
        """
        Return coordinates of random valid pawn.
        """
        return choice(board.get_possible_pawns(self))

    def get_selected_target(self, pawn, board, inteface):
        """
        Return coordinates of random valid target.
        """
        return choice(board.get_all_max_paths(pawn))


class SmartBot(Player):
    def __init__(self, id):
        self.id = id
        self.bot = True

    def get_selected_pawn(self, board, interface):
        """
        Selects pawn using priority rules:
        1: Pawns that can block enemy home row.
        2: Other pawns.
        """
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

        secondary_pawns = []
        for pawn in possible_pawns:
            if pawn not in primary_pawns:
                secondary_pawns.append(pawn)

        if primary_pawns != []:
            return choice(primary_pawns)
        else:
            return choice(secondary_pawns)

    def get_selected_target(self, pawn, board, teminal):
        """
        Selects target using priority rules:
        Neutron:
        1: Home row (instant win).
        2: Not enemy home row.
        3: Targets that can't go to enemy home row in next turn.
        4: Other targets.
        Pawns:
        1: Enemy home row (block).
        2: Other targets.
        """

        if self.get_id() == 1:
            enemy_row = 0
            home_row = 4
        else:
            enemy_row = 4
            home_row = 0

        if pawn == board.get_neutron():
            if self.get_id() == 1:
                enemy_row = 0
                home_row = 4
            else:
                enemy_row = 4
                home_row = 0

            primary_targets = []
            for (row, column) in board.get_all_max_paths(pawn):
                if row == home_row:
                    primary_targets.append((row, column))

            secondary_targets = []
            for (row, column) in board.get_all_max_paths(pawn):
                if row != enemy_row and (row, column) not in primary_targets:
                    secondary_targets.append((row, column))

            tertiary_targets = []
            for (row, column) in board.get_all_max_paths(pawn):
                if (row, column) not in primary_targets and (row, column) not in secondary_targets:
                    tertiary_targets.append((row, column))
        else:
            primary_targets = []
            for (row, column) in board.get_all_max_paths(pawn):
                if row == enemy_row:
                    primary_targets.append((row, column))

            secondary_targets = []
            for (row, column) in board.get_all_max_paths(pawn):
                if (row, column) not in primary_targets:
                    secondary_targets.append((row, column))

            tertiary_targets = []

        if primary_targets != []:
            return choice(primary_targets)
        elif secondary_targets != []:
            return choice(secondary_targets)
        else:
            return choice(tertiary_targets)