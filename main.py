import pygame
import sys
import hashlib
import os
import pygame.image


from const import *

WIDTH = 729 # 3^6
HEIGHT = 729

BG_COLOR = (0, 255, 0)
LINE_COLOR = (23, 145, 135)
CROSS_COLOR = (200, 66, 100)
CIRCLE_COLOR = (239, 231, 200)
FADE = (28, 170, 156)

ALPHA = 100

DIM = 3

class BoardDim:

    def __init__(self, size, xcor, ycor):
        self.size = size
        self.sqsize = size // DIM
        self.xcor = xcor
        self.ycor = ycor

class Board:

    def __init__(self, dims=None, linewidth=15, ultimate=False, max=False):
        self.squares = [ [0, 0, 0] for row in range(DIM)]
        self.dims = dims

        if not dims: 
            self.dims = BoardDim(WIDTH, 0, 0)

        self.linewidth = linewidth
        self.offset = self.dims.sqsize * 0.2
        self.radius = (self.dims.sqsize // 2) * 0.7
        self.max = max

        if ultimate: 
            self.create_ultimate()

        self.active = True

    def __str__(self):
        s = ''
        for row in range(DIM):
            for col in range(DIM):
                sqr = self.squares[row][col]
                s += str(sqr)
        return s

    def create_ultimate(self):
        for row in range(DIM):
            for col in range(DIM):

                size = self.dims.sqsize
                xcor, ycor = self.dims.xcor + (col * self.dims.sqsize), self.dims.ycor + (row * self.dims.sqsize)
                dims = BoardDim(size=size, xcor=xcor, ycor=ycor)
                linewidth = self.linewidth - 7
                ultimate = self.max

                self.squares[row][col] = Board(dims=dims, linewidth=linewidth, ultimate=ultimate, max=False)
    
    def render(self, surface):
        for row in range(DIM):
            for col in range(DIM):
                sqr = self.squares[row][col]

                if isinstance(sqr, Board): sqr.render(surface)
        
        pygame.draw.line(surface, LINE_COLOR, (self.dims.xcor + self.dims.sqsize, self.dims.ycor),                  (self.dims.xcor + self.dims.sqsize, self.dims.ycor + self.dims.size), self.linewidth)
        pygame.draw.line(surface, LINE_COLOR, (self.dims.xcor + self.dims.size - self.dims.sqsize, self.dims.ycor), (self.dims.xcor + self.dims.size - self.dims.sqsize, self.dims.ycor + self.dims.size), self.linewidth)

        pygame.draw.line(surface, LINE_COLOR, (self.dims.xcor, self.dims.ycor + self.dims.sqsize),                  (self.dims.xcor + self.dims.size, self.dims.ycor + self.dims.sqsize), self.linewidth)
        pygame.draw.line(surface, LINE_COLOR, (self.dims.xcor, self.dims.ycor + self.dims.size - self.dims.sqsize), (self.dims.xcor + self.dims.size, self.dims.ycor + self.dims.size - self.dims.sqsize), self.linewidth)

    def valid_sqr(self, xclick, yclick):

        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        sqr = self.squares[row][col]


        if not isinstance(sqr, Board):
            return sqr == 0 and self.active


        return sqr.valid_sqr(xclick, yclick)

    def mark_sqr(self, xclick, yclick, player):
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        sqr = self.squares[row][col]

        print('marking -> (', row, col, ')')


        if not isinstance(sqr, Board):
            self.squares[row][col] = player
            return

        sqr.mark_sqr(xclick, yclick, player)

    def draw_fig(self, surface, xclick, yclick):
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        sqr = self.squares[row][col]


        if not isinstance(sqr, Board):


            if sqr == 1:

                ipos = (self.dims.xcor + (col * self.dims.sqsize) + self.offset, 
                        self.dims.ycor + (row * self.dims.sqsize) + self.offset)
                fpos = (self.dims.xcor + self.dims.sqsize * (1 + col) - self.offset, 
                        self.dims.ycor + self.dims.sqsize * (1 + row) - self.offset)
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth)

                ipos = (self.dims.xcor + (col * self.dims.sqsize) + self.offset, 
                        self.dims.ycor + self.dims.sqsize * (1 + row) - self.offset)
                fpos = (self.dims.xcor + self.dims.sqsize * (1 + col) - self.offset, 
                        self.dims.ycor + (row * self.dims.sqsize) + self.offset)
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth)
            

            elif sqr == 2:
                center = (self.dims.xcor + self.dims.sqsize * (0.5 + col),
                          self.dims.ycor + self.dims.sqsize * (0.5 + row))

                pygame.draw.circle(surface, CIRCLE_COLOR, center, self.radius, self.linewidth)

            return


        sqr.draw_fig(surface, xclick, yclick)

    def manage_win(self, surface, winner, onmain=False):

        transparent = pygame.Surface( (self.dims.size, self.dims.size) )
        transparent.set_alpha( ALPHA )
        transparent.fill( FADE )
        if onmain: 
            surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
            surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
        surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
        

        if not onmain:

            if winner == 1:

                ipos = (self.dims.xcor + self.offset, 
                        self.dims.ycor + self.offset)
                fpos = (self.dims.xcor + self.dims.size - self.offset, 
                        self.dims.ycor + self.dims.size - self.offset)
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth + 7)


                ipos = (self.dims.xcor + self.offset, 
                        self.dims.ycor + self.dims.size - self.offset)
                fpos = (self.dims.xcor + self.dims.size - self.offset, 
                        self.dims.ycor + self.offset)
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth + 7)


            if winner == 2:
                center = (self.dims.xcor + self.dims.size * 0.5,
                        self.dims.ycor + self.dims.size * 0.5)

                pygame.draw.circle(surface, CIRCLE_COLOR, center, self.dims.size * 0.4, self.linewidth + 7)


        self.active = False

    def check_draw_win(self, surface,):

        isfull = True

        for row in range(DIM):
            for col in range(DIM):

                   
                sqr = self.squares[row][col]

                if isinstance(sqr, Board) and sqr.active:

                    winner = sqr.check_draw_win(surface)
                    if winner: 
                        self.squares[row][col] = winner
                        sqr.manage_win(surface, winner)


                for c in range(DIM):
                    if self.squares[0][c] == self.squares[1][c] == self.squares[2][c] != 0:
                        color = CROSS_COLOR if self.squares[0][c] == 1 else CIRCLE_COLOR
                        # draw win
                        ipos = (self.dims.xcor + self.dims.sqsize * (0.5 + c), 
                                self.dims.ycor + self.offset)
                        fpos = (self.dims.xcor + self.dims.sqsize * (0.5 + c), 
                                self.dims.ycor + self.dims.size - self.offset)
                        pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                        return self.squares[0][c]


                for r in range(DIM):
                    if self.squares[r][0] == self.squares[r][1] == self.squares[r][2] != 0:
                        color = CROSS_COLOR if self.squares[r][0] == 1 else CIRCLE_COLOR

                        ipos = (self.dims.xcor + self.offset, 
                                self.dims.ycor + self.dims.sqsize * (r + 0.5))
                        fpos = (self.dims.xcor + self.dims.size - self.offset, 
                                self.dims.ycor + self.dims.sqsize * (r + 0.5))
                        pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                        return self.squares[r][0]


                if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
                    color = CROSS_COLOR if self.squares[1][1] == 1 else CIRCLE_COLOR

                    ipos = (self.dims.xcor + self.offset, 
                            self.dims.ycor + self.offset)
                    fpos = (self.dims.xcor + self.dims.size - self.offset, 
                            self.dims.ycor + self.dims.size - self.offset)
                    pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                    return self.squares[1][1]

                # asc
                if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
                    color = CROSS_COLOR if self.squares[1][1] == 1 else CIRCLE_COLOR
                    # draw win
                    ipos = (self.dims.xcor + self.offset, 
                            self.dims.ycor + self.dims.size - self.offset)
                    fpos = (self.dims.xcor + self.dims.size - self.offset, 
                            self.dims.ycor + self.offset)
                    pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                    return self.squares[1][1]

class Game:

    def __init__(self, ultimate=False, max=False):
        self.ultimate = ultimate
        self.max = max
        self.board = Board(ultimate=ultimate, max=max)
        self.player = 1
        self.playing = True
        pygame.font.init()
        self.return_to_menu = False

    def render_board(self, surface):
        self.board.render(surface)

    def next_turn(self):
        self.player = 2 if self.player == 1 else 1

    def ultimate_winner(self, surface, winner):
        print('ULTIMATE WINNER! ->', winner)

        if winner == 1:
            color = CROSS_COLOR

            iDesc = (WIDTH // 2 - 110, HEIGHT // 2 - 110)
            fDesc = (WIDTH // 2 + 110, HEIGHT // 2 + 110)

            iAsc = (WIDTH // 2 - 110, HEIGHT // 2 + 110)
            fAsc = (WIDTH // 2 + 110, HEIGHT // 2 - 110)

            pygame.draw.line(surface, color, iDesc, fDesc, 22)
            pygame.draw.line(surface, color, iAsc, fAsc, 22)

        else:
            color = CIRCLE_COLOR

            center = (WIDTH // 2, HEIGHT // 2   )
            pygame.draw.circle(surface, color, center, WIDTH // 4, 22)
        
        font = pygame.font.SysFont('monospace', 64)
        lbl = font.render('ULTIMATE WINNER!', 1, color)
        surface.blit(lbl, (WIDTH // 2 - lbl.get_rect().width // 2, HEIGHT // 2 + 220))

        self.playing = False

    def restart(self):
        self.__init__(self.ultimate, self.max)

    def set_return_to_menu(self):
        self.return_to_menu = True
    
    def should_return_to_menu(self):
        return self.return_to_menu



class Menu:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Menu')
        pygame.font.init()  
        self.font = pygame.font.SysFont('monospace', 40)
        self.menu_options = ["Classic", "Ultimate", "Max"]
        self.selected_option = 0

    def draw_menu(self):
        self.screen.blit(background_image, (0, 0))
        #self.screen.fill(BG_COLOR)
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            label = self.font.render(option, 1, color)
            self.screen.blit(label, (WIDTH // 2 - label.get_rect().width // 2, HEIGHT // 4 + i * 60))

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        return self.selected_option

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_menu()
            pygame.display.update()

class StartMenu:

    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont('monospace', 40)
        self.menu_options = ["Start Game", "Quit"]
        self.selected_option = 0

    def draw_menu(self):
        #self.screen.fill(BG_COLOR)
        self.screen.blit(background_image, (0, 0))
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            label = self.font.render(option, 1, color)
            self.screen.blit(label, (WIDTH // 2 - label.get_rect().width // 2, HEIGHT // 4 + i * 60))

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        return self.selected_option

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_menu()
            pygame.display.update()

class ColorMenu:

    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont('monospace', 40)
        self.colors = ["Green", "Red", "Blue"]
        self.selected_color = 0

    def draw_menu(self):
        #self.screen.fill(BG_COLOR)
        self.screen.blit(background_image, (0, 0))
        for i, color in enumerate(self.colors):
            text_color = (255, 255, 255) if i == self.selected_color else (100, 100, 100)
            label = self.font.render(color, 1, text_color)
            self.screen.blit(label, (WIDTH // 2 - label.get_rect().width // 2, HEIGHT // 4 + i * 60))

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_color = (self.selected_color + 1) % len(self.colors)
                    elif event.key == pygame.K_UP:
                        self.selected_color = (self.selected_color - 1) % len(self.colors)
                    elif event.key == pygame.K_RETURN:
                        return self.colors[self.selected_color]

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_menu()
            pygame.display.update()



class StartMenu:

    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont('monospace', 40)
        self.menu_options = ["Start Game",  "Quit"]  
        self.selected_option = 0

    def draw_menu(self):
        #self.screen.fill(BG_COLOR)
        self.screen.blit(background_image, (0, 0))
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            label = self.font.render(option, 1, color)
            self.screen.blit(label, (WIDTH // 2 - label.get_rect().width // 2, HEIGHT // 4 + i * 60))

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        return self.selected_option

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_menu()
            pygame.display.update()

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.SysFont('monospace', 40)
        self.username = ""
        self.password = ""
        self.is_logging_in = True
        self.username_selected = True  
        self.password_selected = False  
        self.error_message = ""
        self.error_font = pygame.font.SysFont('monospace', 30)

        # List of user credentials (username and hashed password)
        self.user_credentials = [
            {"username": "user1", "password_hash": hashlib.sha256("password1".encode()).hexdigest()},
            {"username": "user2", "password_hash": hashlib.sha256("password2".encode()).hexdigest()},
            {"username": "filip", "password_hash": hashlib.sha256("parola".encode()).hexdigest()},
            # Add more usernames and hashed passwords as needed
        ]

    def authenticate_user(self):
        username = self.username.strip()
        password = self.password.strip()

        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()

        for user in self.user_credentials:
            if user["username"] == username and user["password_hash"] == entered_password_hash:
                self.is_logging_in = False
                return True

        self.error_message = "Incorrect username or password"
        self.username = ""
        self.password = ""
        return False

    def draw_login_screen(self):
        #self.screen.fill(BG_COLOR)
        self.screen.blit(background_image, (0, 0))

        label_username = self.font.render(f"Username: {self.username}", 1, (255, 255, 255))
        label_password = self.font.render(f"Password: {len(self.password)*'*'}", 1, (255, 255, 255))
        self.screen.blit(label_username, (WIDTH // 2 - label_username.get_rect().width // 2, HEIGHT // 4))
        self.screen.blit(label_password, (WIDTH // 2 - label_password.get_rect().width // 2, HEIGHT // 2))

    def draw_error_message(self):
        if self.error_message:
            error_label = self.error_font.render(self.error_message, 1, (255, 0, 0))
            self.screen.blit(error_label, (WIDTH // 2 - error_label.get_rect().width // 2, HEIGHT // 2 + 50))

    def run_login_screen(self):
        while self.is_logging_in:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.username) > 0 and self.username_selected:
                            self.username = self.username[:-1]
                        elif len(self.password) > 0 and self.password_selected:
                            self.password = self.password[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.authenticate_user():
                            return not self.is_logging_in
                    elif event.key == pygame.K_ESCAPE:
                        self.is_logging_in = False
                    elif event.key == pygame.K_TAB:
                        self.username_selected = not self.username_selected
                        self.password_selected = not self.password_selected
                    elif event.unicode and (self.username_selected or self.password_selected):
                        if self.username_selected:
                            self.username += event.unicode
                        elif self.password_selected:
                            self.password += event.unicode

            self.draw_login_screen()
            self.draw_error_message()
            pygame.display.update()

        return not self.is_logging_in


background_image = pygame.image.load(r'C:\Users\filip\Downloads\geometric-Blue-Wallpaper-Free-Download.jpg')
        # Resize the image to match the screen size
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('ULTIMATE TIC TAC TOE')
        
        # Blit the image onto the screen
        self.screen.blit(background_image, (0, 0))
        self.login_screen = LoginScreen(self.screen)
        self.start_menu = StartMenu(self.screen)
        self.game = None
        self.logged_in = False  
        

    def mainloop(self):
        while True:
            if not self.logged_in:
                self.logged_in = self.login_screen.run_login_screen()
            else:
                start_menu_option = self.start_menu.run_menu()
            if not self.logged_in:
                self.logged_in = self.login_screen.run_login_screen()
            else:
                start_menu_option = self.start_menu.run_menu()

                if start_menu_option == 0:
                    mode = self.show_mode_selection_menu()
                    if mode is None:
                        continue

                    if mode == 0:  
                        self.game = Game()
                    elif mode == 1:  
                        self.game = Game(ultimate=True, max=False)
                    elif mode == 2:  
                        self.game = Game(ultimate=True,max=True)
                    #self.screen.fill(BG_COLOR)
                    self.screen.blit(background_image, (0, 0))
                    self.game.render_board(self.screen)
                    pygame.display.update()

                    while self.game.playing:
                        self.handle_game_events()

                        pygame.display.update()

                        if self.game.should_return_to_menu():
                            break

                    self.handle_game_over()

                elif start_menu_option == 1 and self.game is not None:
                    self.show_customize_menu()

                elif start_menu_option == 2:
                    pygame.quit()
                    sys.exit()


    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_color = (self.selected_color + 1) % len(self.colors)
                    elif event.key == pygame.K_UP:
                        self.selected_color = (self.selected_color - 1) % len(self.colors)
                    elif event.key == pygame.K_RETURN:
                        return self.colors[self.selected_color]

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_menu()
            pygame.display.update()

    def show_customize_menu(self):
        #global BG_COLOR  

        customize_menu = Menu()
        customize_menu.menu_options = ["Select Background Color", "Go Back"]
        customize_menu.selected_option = 0

        selected_color = "Green"  

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        customize_menu.selected_option = (customize_menu.selected_option + 1) % len(customize_menu.menu_options)
                    elif event.key == pygame.K_UP:
                        customize_menu.selected_option = (customize_menu.selected_option - 1) % len(customize_menu.menu_options)
                    elif event.key == pygame.K_RETURN:
                        customize_option = customize_menu.selected_option

                        if customize_option == 0:  
                            color_menu = ColorMenu(self.screen)
                            selected_color = color_menu.run_menu()

                            if selected_color == "Green":
                                BG_COLOR = (0, 255, 0)
                            elif selected_color == "Red":
                                BG_COLOR = (255, 0, 0)
                            elif selected_color == "Blue":
                                BG_COLOR = (0, 0, 255)

                            
                            #self.screen.fill(BG_COLOR)
                            self.screen.blit(background_image, (0, 0))
                            self.game.render_board(self.screen)
                            pygame.display.update()

                        elif customize_option == 1:  
                            return

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            customize_menu.draw_menu()
            pygame.display.update()




    def show_mode_selection_menu(self):
        mode_menu = StartMenu(self.screen)
        mode_menu.menu_options = ["Classic", "Ultimate", "Max"]
        return mode_menu.run_menu()

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                xclick, yclick = event.pos

                if self.game.board.valid_sqr(xclick, yclick):
                    self.game.board.mark_sqr(xclick, yclick, self.game.player)

                    winner = self.game.board.check_draw_win(self.screen)
                    if winner:
                        self.game.board.manage_win(self.screen, winner, onmain=True)
                        self.game.ultimate_winner(self.screen, winner)

                    self.game.board.draw_fig(self.screen, xclick, yclick)

                    self.game.next_turn()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.restart()
                    self.screen.fill(BG_COLOR)
                    self.game.render_board(self.screen)

                if event.key == pygame.K_m:
                    self.game.set_return_to_menu()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_game_over(self):
        pygame.time.delay(1000)
        self.screen.fill(BG_COLOR)
        pygame.display.update()
        self.game.return_to_menu = False


if __name__ == '__main__':
    main = Main()
    main.mainloop()
