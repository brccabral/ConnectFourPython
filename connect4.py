# %%
# pip install numpy
import numpy as np
# pip install pygame
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2-5)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    # Check for positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    # Check for negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    board = np.flip(board, 0)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # surface, color, (top left x, top left y, width, height)
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            else:
                color = BLACK
            # surface, color, (center x, center y), radius
            pygame.draw.circle(screen, color, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board = create_board()
game_over = False # True = someone wins (4 in a row)
turn = 0 # 0 - p1 turn

pygame.init()

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            # resets the first bar to all black so it can draw the piece circle just once
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            (posx, posy) = event.pos
            if turn == 0:
                color = RED
            else:
                color = YELLOW
            pygame.draw.circle(screen, color, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # resets the top to display message if game over
            # if game continues, it will draw piece from pygame.MOUSEMOTION
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            (posx, posy) = event.pos
            col = int(math.floor(posx/SQUARESIZE))
            # # Ask for Player 1 input
            if turn == 0:
                # col = int(input("Player 1 make your selection (0-6):"))
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        print("Player 1 Wins!")
                        label = myfont.render("Player 1 Wins!", 1, RED)
                        # label, (top left x, y)
                        screen.blit(label, (40,10))
                        game_over = True

            # # Ask for Player 2 input
            else:
            #     col = int(input("Player 2 make your selection (0-6):"))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        print("Player 2 Wins!")
                        label = myfont.render("Player 2 Wins!", 1, YELLOW)
                        # label, (top left x, y)
                        screen.blit(label, (40,10))
                        game_over = True
            turn += 1
            turn = turn % 2
            draw_board(board)
            print_board(board)
            
            if game_over:
                pygame.time.wait(3000)