from errors import WrongPawn, WrongData, WrongCoordinates, WrongTarget, BlockedPawn
import pygame
import sys


class TextInterface:
    def __init__(self, board):
        self.board = board

    def select_pawn(self, player, test=None):
        """
        Asks player for coordinates of chosen pawn.
        Returns coordinates (tuple).
        """
        if test is None:
            _pawn = input("Select pawn (row, column):\n").replace(" ", "")
        else:
            _pawn = test
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

    def select_target(self, pawn, test=None):
        """
        Asks player for coordinates of chosen target.
        Returns coordinates (tuple).
        """
        if test is None:
            _target = input("Select target (row, column):\n").replace(" ", "")
        else:
            _target = test
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

    def select_game_mode(self):
        """
        Asks player for game mode.
        Returns game mode id (int).
        """
        mode_chose = False
        while not mode_chose:
            try:
                print("\033[93mChoose game mode:\n1: One player mode with easy computer\n2: One player mode with hard computer\n3: Two players mode\n4: AI mode\033[0m")
                game_mode = input()
            except KeyboardInterrupt:
                sys.exit()
            except EOFError:
                sys.exit()

            if game_mode in ["1", "2", "3", "4"]:
                mode_chose = True
            else:
                print("Invalid input. Try again.")
        return game_mode

    def select_game_end(self, winner):
        """
        Asks player how to end the game.
        Returns winner id or exits the game.
        """
        game_end_chose = False
        while not game_end_chose:
            try:
                print("\033[93mDo you want to end the game?\n1: Yes\n2: No\033[0m")
                game_end = input()
            except KeyboardInterrupt:
                sys.exit()
            except EOFError:
                sys.exit()

            if game_end == "1":
                sys.exit(0)
            elif game_end == "2":
                return winner
                game_end_chose = True
            else:
                print("Invalid input. Try again.")

    def print_error(self, error):
        print(f"\033[91m{error}\033[0m")

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

    def print_background(self):
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

    def print_header(self, header):
        print(f"\033[93m{header}\033[0m")
        print()
        self.print_background()

    def print_winner(self, winner):
        print()
        if winner == 1:
            print("\033[93mPlayer 1 wins...\033[0m")
        elif winner == 2:
            print("\033[93mPlayer 2 wins...\033[0m")
        else:
            print("\033[93mDraw...\033[0m")


class GUI:
    def __init__(self, board):
        pygame.init()

        self.board = board
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Neutron')
        try:
            self.load_images()
        except Exception:
            print(f"\033[91mCannot load images\033[0m")
            sys.exit()

    def load_images(self):
        """
        Loads all images.
        """
        self.image_board = pygame.image.load("images/board.png")
        self.menu = pygame.image.load("images/menu.png")
        self.log = pygame.image.load("images/log.png")

        self.red_pawn = pygame.image.load("images/r_pawn.png")
        self.green_pawn = pygame.image.load("images/g_pawn.png")
        self.blue_pawn = pygame.image.load("images/b_pawn.png")
        self.active_pawn = pygame.image.load("images/active_pawn.png")
        self.selected_pawn = pygame.image.load("images/selected_pawn.png")
        self.selected_target = pygame.image.load("images/selected_target.png")

    def select_pawn(self, player):
        """
        Waits for selecting pawn or exiting the game.
        Returns coordinates (tuple).
        """
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
        """
        Waits for selecting target or exiting the game.
        Returns coordinates (tuple).
        """
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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

    def select_game_mode(self):
        """
        Draws game menu and wait for selecting game mode or exiting the game.
        Returns game mode id (int).
        """
        # Background
        self.screen.blit(self.menu, (0, 0))

        font = pygame.font.match_font("Calibri", bold=True)
        font = pygame.font.Font(font, 32)

        header = "NEUTRON"
        text = font.render(header, True, (255, 255, 0))
        textRect = text.get_rect()
        textRect.center = (300, 50)
        self.screen.blit(text, textRect)

        texts = [
            ("Choose game mode:", (0, 0, 0)),
            ("One player mode with easy computer", (0, 100, 0)),
            ("One player mode with hard computer", (0, 120, 0)),
            ("Two players mode:", (0, 140, 0))
        ]
        for line in range(len(texts)):
            text = font.render(texts[line][0], True, texts[line][1])
            textRect = text.get_rect()
            textRect.center = (300, 150 + line * 100)
            self.screen.blit(text, textRect)
        pygame.display.update()

        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if y >= 220 and y <= 270:
                        return 1
                    elif y >= 320 and y <= 370:
                        return 2
                    elif y >= 420 and y <= 470:
                        return 3

    def select_game_end(self, winner):
        """
        Draws end game menu and wait for selecting game end or exiting the game.
        Returns winner id (int).
        """
        # Background
        self.screen.blit(self.menu, (0, 0))

        font = pygame.font.match_font("Calibri", bold=True)
        font = pygame.font.Font(font, 32)

        self.print_winner(winner, table=False)

        texts = [
            ("Do you want to end the game?", (0, 0, 0)),
            ("Yes", (0, 100, 0)),
            ("No", (0, 120, 0)),
        ]
        for line in range(len(texts)):
            text = font.render(texts[line][0], True, texts[line][1])
            textRect = text.get_rect()
            textRect.center = (300, 150 + line * 100)
            self.screen.blit(text, textRect)
        pygame.display.update()

        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if y >= 220 and y <= 270:
                        return None
                    elif y >= 320 and y <= 370:
                        return winner

    def print_error(self, error):
        self.screen.blit(self.log, (0, 550))
        font = pygame.font.match_font("Calibri", bold=True)
        font = pygame.font.Font(font, 32)
        text = font.render(error, True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (300, 575)
        self.screen.blit(text, textRect)

        pygame.display.update()

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

    def print_possible_pawns(self, player):
        base_x = 60
        shift_x = 100
        base_y = 60
        shift_y = 100

        for row in range(len(self.board.get_board())):
            for column in range(len(self.board.get_board()[row])):
                if (row, column) in self.board.get_possible_pawns(player):
                    self.screen.blit(self.active_pawn, (base_x + column * shift_x, base_y + row * shift_y))
        pygame.display.update()

    def print_background(self):
        base_x = 60
        shift_x = 100
        base_y = 60
        shift_y = 100

        # Table
        self.screen.blit(self.image_board, (0, 0))

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

    def print_header(self, header, table=True):
        if table:
            self.print_background()
        else:
            self.screen.blit(self.menu, (0, 0))

        font = pygame.font.match_font("Calibri", bold=True)
        font = pygame.font.Font(font, 32)
        text = font.render(header, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (300, 25)
        self.screen.blit(text, textRect)

        pygame.display.update()

    def print_winner(self, winner, table=True):
        if winner == 1:
            self.print_header("Player 1 wins...", table)
        elif winner == 2:
            self.print_header("Player 2 wins...", table)
        else:
            self.print_header("Draw...", table)
