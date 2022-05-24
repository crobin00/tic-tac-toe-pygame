import pygame, random, sys
from pygame.locals import *
pygame.init()

font = pygame.font.Font('ARCADECLASSIC.ttf', 80)
fontsmall = pygame.font.Font('ARCADECLASSIC.ttf', 40)
fontsmallest = pygame.font.Font('ARCADECLASSIC.ttf', 20)

class Button:
    def __init__(self, x, y, width, height, font, text, bg_color, hovering_color, font_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.bg_color = bg_color
        self.font_color = font_color
        self.current_color = bg_color
        self.text = text 
        self.hovering_color = hovering_color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(WINDOW, self.current_color, self.rect)
        text = self.font.render(self.text, True, self.font_color)
        text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))

        WINDOW.blit(text, text_rect)

    def isHovering(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.current_color = self.hovering_color
        else:
            self.current_color = self.bg_color

    def isClicked(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False



class Board:
    def __init__(self):
        self.board = [[0,0,0],[0,0,0],[0,0,0]] 

    def create(self, window):
        horiz1Start = (250, 50)
        horiz1End = (250, 650)
        horiz2Start = (450, 50)
        horiz2End = (450, 650)
        vert1Start = (50, 250)
        vert1End = (650, 250)
        vert2Start = (50, 450)
        vert2End = (650, 450)
        pygame.draw.line(window,BLACK,horiz1Start,horiz1End) 
        pygame.draw.line(window,BLACK,horiz2Start,horiz2End) 
        pygame.draw.line(window,BLACK,vert1Start,vert1End) 
        pygame.draw.line(window,BLACK,vert2Start,vert2End) 

    def placePiece(self, row, col, player):
        self.board[row][col] = player

    def isEmptySpace(self, row, col):
        if self.board[row][col] == 0:
            return True
        return False

    def draw(self, window):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 1:
                    x1Start = (50 + (col * 200 + 10), 50 + (row * 200 + 10))
                    x1End = (50 + ((col + 1) * 200 - 10),50 + ((row + 1) * 200 - 10))
                    x2Start = (50 + ((col + 1) * 200 - 10), 50 + (row * 200 + 10))
                    x2End = (50 + (col * 200 + 10),50 + ((row + 1) * 200 - 10))
                    pygame.draw.line(window,XCOLOR,x1Start, x1End, 10)
                    pygame.draw.line(window,XCOLOR,x2Start, x2End, 10)
                elif self.board[row][col] == 2:
                    circleCenter = (50 + (col * 200 + 100), 50 + (row * 200 + 100))
                    pygame.draw.circle(window,OCOLOR,circleCenter,90, 10)
                else:
                    pass

    def drawHorizontal(self, col):
        start = (60, 50 + (col * 200 + 100))
        end = (640, 50 + (col * 200 + 100))
        pygame.draw.line(WINDOW, BLACK, start, end)

    def drawVertical(self, row):
        start = (50 + (row * 200 + 100), 60)
        end = (50 + (row * 200 + 100), 640)
        pygame.draw.line(WINDOW, BLACK, start, end)

    def drawDiagonal(self, pos):
        if pos == 'back':
            pygame.draw.line(WINDOW, BLACK, (640, 50), (50, 640), 20)

        if pos == 'forward':
            pygame.draw.line(WINDOW, BLACK, (50, 50), (640, 640), 20)

    def checkTie(self):
        for col in range(3):
            for row in range(3):
                if self.board[row][col] == 0:
                    return False

        return True

    def checkWin(self, player):
        won = False
        # Horizontal and vertical win
        for i in range(3):
            if self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player:
                won = True
                self.drawHorizontal(i)
                print("horiz")
            if self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == player:
                won = True
                self.drawVertical(i)
                print("vert")

        # Diagonal Wins
        for i in range(1):
            if self.board[i][i] == player and self.board[i+1][i+1] == player and self.board[i+2][i+2] == player:
                won = True
                self.drawDiagonal('forward')
                print("diag")
            if self.board[i][i+2] == player and self.board[i+1][i+1] == player and self.board[i+2][i] == player:
                won = True
                self.drawDiagonal('back')
                print("diag")
                
        return won

    def resetBoard(self, window):
        global gameOver, currentTurn
        for row in range(3):
            for col in range(3):
                self.board[row][col] = 0

        window.fill(PINK)
        self.create(window)
        gameOver = False
        currentTurn = True

class Player:
    def __init__(self, piece):
        if piece == 'X':
            self.piece = 1
        if piece == 'O':
            self.piece = 2

    def placePiece(self, board, row, col):
        board.placePiece(row, col, self.piece)

    def placeRandom(self, board):
        while True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if board.isEmptySpace(row, col):
                board.placePiece(row, col, self.piece)
                return
        

def main_menu():
    global CPU
    onePlayerButton = Button(SCREEN_WIDTH / 2 - 125, 300, 250, 60, fontsmall, "One player", PURPLE, LIGHTPURPLE, WHITE)
    twoPlayerButton = Button(SCREEN_WIDTH / 2 - 125, 450, 250, 60, fontsmall, "Two Player", PURPLE, LIGHTPURPLE, WHITE)
    while True:
        WINDOW.fill(PINK)
        mousePos = pygame.mouse.get_pos()

        title = font.render("Tic Tac Toe", True, BLACK)
        WINDOW.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 100))
        
        for button in [onePlayerButton, twoPlayerButton]:
            button.isHovering(mousePos)
            button.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if onePlayerButton.isClicked(mousePos):
                    print("one player")
                    CPU = True
                    game()
                if twoPlayerButton.isClicked(mousePos):
                    print("two player")
                    CPU = False
                    game()

        pygame.display.update()
        clock.tick(FPS)


def game():
    global gameOver, currentTurn
    WINDOW.fill(PINK)
    board.create(WINDOW)
    resetButton = Button(600, 0, 100, 50, fontsmallest, "RESET", PURPLE, LIGHTPURPLE, WHITE)
    mainMenuButton = Button(0, 0, 100, 50, fontsmallest, "MAINMENU", PURPLE, LIGHTPURPLE, WHITE)
    while True:
        mousePos = pygame.mouse.get_pos()
        for button in [resetButton, mainMenuButton]:
            button.isHovering(mousePos)
            button.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and not gameOver:
                row = (event.pos[1] - 50) // 200
                col = (event.pos[0] - 50) // 200
                print(row, col)
                if row == 3: row = 2
                if col == 3: col = 2
                if row == -1: row = 0
                if col == -1: col = 0
                print(row, col)
                if event.button == 1 and board.isEmptySpace(row, col):
                    if currentTurn:
                        player.placePiece(board, row, col)
                        print(currentTurn)
                        gameOver = board.checkWin(player.piece) or board.checkTie()
                    if not currentTurn and not CPU:
                        opponent.placePiece(board,row, col)
                        gameOver = board.checkWin(opponent.piece) or board.checkTie()
                    currentTurn = not currentTurn
                    print(board.board)
            if event.type == MOUSEBUTTONDOWN:
                if mainMenuButton.isClicked(mousePos):
                    board.resetBoard(WINDOW)
                    main_menu()
                if resetButton.isClicked(mousePos):
                    board.resetBoard(WINDOW)
            if event.type == KEYDOWN:
                if event.key == pygame.K_r:
                    board.resetBoard(WINDOW)

        if not currentTurn and CPU and not gameOver:
            opponent.placeRandom(board)
            gameOver = board.checkWin(opponent.piece) or board.checkTie()
            currentTurn = not currentTurn
        board.draw(WINDOW)

        pygame.display.update()
        clock.tick(FPS)
    

FPS = 30
clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (194, 175, 224)
PURPLE = (98, 4, 112)
LIGHTPURPLE = (222, 0, 255)
XCOLOR = (37, 20, 64)
OCOLOR = (77, 55, 110)

# Screen Information
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700


WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

board = Board()

player = Player('X')
opponent = Player('O')
currentTurn = True
gameOver = False
CPU = False

main_menu()
