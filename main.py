from random import choice
from errors import WrongPawn, WrongData, WrongCoordinates, WrongTarget, BlockedPawn
from sys import exit
from colorama import init as colorinit
from os import system
from time import sleep
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
        Returns target infor pawn on given coordinates.
        :param tuple of ints origin_coordinates: Coordinates of pawn.
        """

        vector_row, vector_column = vector
        origin_row, origin_column = origin_coordinates

        if not self.validate_coordinates((origin_row + vector_row, origin_column + vector_column)):
            return origin_coordinates
        if self.get_pawn((origin_row + vector_row, origin_column + vector_column)) != 0:
            return origin_coordinates
        else:
            return self.get_max_directed_path((origin_row + vector_row, origin_column + vector_column), vector)


# Interfaces
class TextInterface:
    def __init__(self, board):
        self.board = board

    def select_pawn(self, player):
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
        if not self.board.validate_coordinates(tuple(_coordinates)):
            raise WrongCoordinates

        # Not valid pawn
        if self.board.get_pawn(_coordinates) != player.get_id():
            raise WrongPawn

        # Blocked
        if tuple(_coordinates) not in self.board.get_possible_pawns(player):
            raise BlockedPawn

        return tuple(_coordinates)

    def select_target(self, pawn):
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
        if not self.board.validate_coordinates(tuple(_coordinates)):
            raise WrongCoordinates

        # Not valid target
        if tuple(_coordinates) not in self.board.get_all_max_paths(pawn):
            raise WrongTarget

        return tuple(_coordinates)

    def print_all_max_paths(self, origin_coordinates):
        print(f"Possible targets:")
        for path in self.board.get_all_max_paths(origin_coordinates)[:-1]:
            print(f"{path}, ", end="")
        print(f"{self.board.get_all_max_paths(origin_coordinates)[-1]}")

    def print_possible_pawns(self, player):
        print(f"Possible pawns:")
        for pawn in self.board.get_possible_pawns(player)[:-1]:
            print(f"{pawn}, ", end="")
        print(f"{self.board.get_possible_pawns(player)[-1]}")

    def print_all(self, **kwargs):
        # Header
        if "player" in kwargs.keys() and "neutron" in kwargs.keys():
            print(f"\033[93mNeutron's Turn (Player {kwargs['player'].get_id()})\033[0m\n")
        elif "player" in kwargs.keys():
            print(f"\033[93mPlayer's {kwargs['player'].get_id()} Turn\033[0m\n")
        elif "winner" in kwargs.keys():
            if kwargs["winner"] == 1:
                print("\033[33mPlayer 1 wins...\033[0m")
            elif kwargs["winner"] == 2:
                print("\033[33mPlayer 2 wins...\033[0m")
            elif kwargs["winner"] == 3:
                print("\033[33mDraw...\033[0m")

        # Board
        print(f"  ", end="")
        for col in range(5):
            print(f" \033[93m{col}\033[0m ", end="")
        print()

        for row in range(5):
            print(f"\033[93m{row}\033[0m ", end="")
            for col in range(5):
                if self.board.get_pawn((row, col)) == 1:
                    print(f" \033[92m1\033[0m ", end="")
                elif self.board.get_pawn((row, col)) == 2:
                    print(f" \033[91m2\033[0m ", end="")
                elif self.board.get_pawn((row, col)) == 3:
                    print(f" \033[94m3\033[0m ", end="")
                else:
                    print(f" {self.board.get_pawn((row, col))} ", end="")
            print()
        print()


class GUI(TextInterface):
    def __init__(self, board):
        pygame.init()

        self.board = board
        self.image_board = pygame.sprite.Group()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Neutron')
        try:
            self.load_images()
        except Exception:
            print(f"\033[91mCannot load images\033[0m")
            exit()

    def load_images(self):
        """
        Loads all images.
        """
        self.image_board = pygame.image.load("images/board.png")
        self.red_pawn = pygame.image.load("images/r_pawn.png")
        self.green_pawn = pygame.image.load("images/g_pawn.png")
        self.blue_pawn = pygame.image.load("images/b_pawn.png")
        self.selected_pawn = pygame.image.load("images/selected_pawn.png")
        self.selected_target = pygame.image.load("images/selected_target.png")

    def select_pawn(self, player):
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    row = (y - 60) // 100
                    column = (x - 60) // 100

                    base_x = 55
                    shift_x = 100
                    base_y = 55
                    shift_y = 100

                    # Coordinates not on board
                    if not self.board.validate_coordinates((row, column)):
                        raise WrongCoordinates

                    # Not valid pawn
                    if self.board.get_pawn((row, column)) != player.get_id():
                        raise WrongPawn

                    # Blocked
                    if (row, column) not in self.board.get_possible_pawns(player):
                        raise BlockedPawn

                    self.screen.blit(self.selected_pawn, (base_x + column * shift_x, base_y + row * shift_y))
                    pygame.display.update()
                    return (row, column)

    def select_target(self, pawn):
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    row = (y - 60) // 100
                    column = (x - 60) // 100

                    # Coordinates not on board
                    if not self.board.validate_coordinates((row, column)):
                        raise WrongCoordinates

                    # Not valid target
                    if (row, column) not in self.board.get_all_max_paths(pawn):
                        raise WrongTarget

                    return (row, column)

    def print_possible_pawns(self, player):
        pass

    def print_all_max_paths(self, origin_coordinates):
        base_x = 55
        shift_x = 100
        base_y = 55
        shift_y = 100

        for row in range(len(self.board.get_board())):
            for column in range(len(self.board.get_board()[row])):
                if (row, column) in self.board.get_all_max_paths(origin_coordinates):
                    self.screen.blit(self.selected_target, (base_x + column * shift_x, base_y + row * shift_y))
        pygame.display.update()

    def print_all(self, **kwargs):
        base_x = 60
        shift_x = 100
        base_y = 60
        shift_y = 100

        # Background
        self.screen.blit(self.image_board, (0, 0))

        # Header
        if "player" in kwargs.keys() and "neutron" in kwargs.keys():
            text = f"Neutron's Turn (Player {kwargs['player'].get_id()})"
        elif "player" in kwargs.keys():
            text = f"Player's {kwargs['player'].get_id()} Turn"
        elif "winner" in kwargs.keys():
            if kwargs["winner"] == 1:
                text = "Player 1 wins..."
            elif kwargs["winner"] == 2:
                text = "Player 2 wins..."
            elif kwargs["winner"] == 3:
                text = "Draw..."

        font = pygame.font.match_font("Calibri", bold=True)
        font = pygame.font.Font(font, 32)
        text = font.render(text, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (300, 25)
        self.screen.blit(text, textRect)

        # Pawns
        for row in range(len(self.board.get_board())):
            for column in range(len(self.board.get_board()[row])):
                if self.board.get_pawn((row, column)) == 1:
                    self.screen.blit(self.red_pawn, (base_x + column * shift_x, base_y + row * shift_y))
                elif self.board.get_pawn((row, column)) == 2:
                    self.screen.blit(self.green_pawn, (base_x + column * shift_x, base_y + row * shift_y))
                elif self.board.get_pawn((row, column)) == 3:
                    self.screen.blit(self.blue_pawn, (base_x + column * shift_x, base_y + row * shift_y))
        
        pygame.display.update()


# Players
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

    def get_selected_pawn(self, board, interface):
        pawn = None
        while pawn is None:
            try:
                return interface.select_pawn(self)
            except WrongData:
                print(f"\033[91m{'You gave wrong data or used wrong format. Try again.'}\033[0m")
            except WrongCoordinates:
                print(f"\033[91m{'You gave wrong coordinates. Try again.'}\033[0m")
            except WrongPawn:
                print(f"\033[91m{'You selected wrong pawn. Try again.'}\033[0m")
            except BlockedPawn:
                print(f"\033[91m{'You selected pawn that is fully blocked. Try again.'}\033[0m")
            except KeyboardInterrupt:
                exit()
            except EOFError:
                exit()

    def get_selected_target(self, pawn, board, interface):
        target = None
        while target is None:
            try:
                return interface.select_target(pawn)
            except WrongData:
                print(f"\033[91m{'You gave wrong data or used wrong format. Try again.'}\033[0m")
            except WrongCoordinates:
                print(f"\033[91m{'You gave wrong coordinates. Try again.'}\033[0m")
            except WrongTarget:
                print(f"\033[91m{'You selected wrong target. Try again.'}\033[0m")
            except KeyboardInterrupt:
                exit()
            except EOFError:
                exit()

    def move_pawn(self, origin_coordinates, target_coordinates, board):
        board.replace(origin_coordinates, target_coordinates)

    def __str__(self):
        return f"Player {self.id}"


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


# Game
class Game:
    def __init__(self, video_mode=0, game_mode=None, first_turn=None):
        self.board = Board()
        self.video_mode = video_mode
        if video_mode == 0:
            self.interface = TextInterface(self.board)
        else:
            self.interface = GUI(self.board)

        if game_mode is not None:
            self.game_mode = game_mode
            if game_mode == 1:
                self.players = [Player(1), RandomBot(2)]
            elif game_mode == 2:
                self.players = [Player(1), SmartBot(2)]
            elif game_mode == 3:
                self.players = [Player(1), Player(2)]
            elif game_mode == 4:
                self.players = [SmartBot(1), SmartBot(2)]
            else:
                self.players, self.game_mode = self.select_game_mode()
        else:
            self.players, self.game_mode = self.select_game_mode()

        if first_turn is not None:
            self.first_turn = first_turn
        else:
            self.first_turn = True

    def select_game_mode(self):
        mode_chose = False
        while not mode_chose:
            try:
                print("\033[93mChoose game mode:\n1: One player mode with easy computer\n2: One player mode with hard computer\n3: Two players mode\n4: AI mode\033[0m")
                mode = input()
            except KeyboardInterrupt:
                exit()
            except EOFError:
                exit()

            if mode == "1":
                mode_chose = True
                return ([Player(1), RandomBot(2)], 1)
            elif mode == "2":
                mode_chose = True
                return ([Player(1), SmartBot(2)], 2)
            elif mode == "3":
                mode_chose = True
                return ([Player(1), Player(2)], 3)
            elif mode == "4":
                mode_chose = True
                return ([SmartBot(1), SmartBot(2)], 4)
            else:
                mode_chose = False
                print("Invalid input. Try again.")

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
    game = Game(video_mode=1, game_mode=4)
    game.play()
