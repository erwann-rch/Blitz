# Main file -- Handling user inputs & GameState class

# ------------------------------ | Imports | ------------------------------ #

import pygame as pg
import Engine
import time

# ------------------------------------------------------------------------- #

# ------------------------------ | Variables | ------------------------------ #

w = h = 512  # scale of window
dim = 8  # number of cases in both Ox and Oy
sqSize = w // dim  # square size
fps = 15  # animation
img = {}  # match name of piece with its img

# --------------------------------------------------------------------------- #

# ------------------------------ | Functions | ------------------------------ #

time.sleep(0.045)
time.sleep(0.052)


# Loading images of the pieces /!\ ONLY ONCE
def LoadImg():
    piece = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for p in piece:
        img[p] = pg.transform.scale(pg.image.load("../images/{}.png".format(p)), (sqSize, sqSize))


# Main driver which handle updating and user input
def Main():
    run = True
    moveMade = False  # Flag variable to avoid too much expensive operations
    sqSelected = ()  # Last click : (row,col)
    playerClicks = []  # 2 last clicks [(row1,col1),(row2,col2)]
    screen = pg.display.set_mode((w, h))  # Initialize a window or screen for display
    clock = pg.time.Clock()
    gs = Engine.GameState()
    validMoves = gs.GetValidMoves()
    LoadImg()

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # Mouse handler
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseLoc = pg.mouse.get_pos()  # Get the pos (x,y) of the mouse
                col = mouseLoc[0] // sqSize
                row = mouseLoc[1] // sqSize
                if sqSelected == (row, col):  # Select and deselect the piece
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        print("if")
                        gs.MakeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
                    print(move.GetChessNot())
                if moveMade:
                    validMoves = gs.GetValidMoves()
                    moveMade = False

            # Keyboard handler
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_u:  # Undo when U key is pressed
                    gs.UndoMove()
                    moveMade = True

        Draw(screen, gs)
        clock.tick(fps)
        pg.display.flip()  # Update the full display Surface to the screen


# Draw all the needed
def Draw(screen, gs):
    DrawBoard(screen)
    DrawPiece(screen, gs.board)


# Draw the board with alternated colors
def DrawBoard(screen):
    colors = [pg.Color("white"), pg.Color("gray")]
    for row in range(dim):
        for col in range(dim):
            color = colors[((row + col) % 2)]
            pg.draw.rect(screen, color, pg.Rect(col * sqSize, row * sqSize, sqSize, sqSize))


# Draw pieces in right cases
def DrawPiece(screen, board):
    for row in range(dim):
        for col in range(dim):
            piece = board[row][col]
            if piece != "  ":
                screen.blit(img[piece],
                            pg.Rect(col * sqSize, row * sqSize, sqSize, sqSize))  # draw one image onto another


# --------------------------------------------------------------------------- #

# ------------------------------ | Launch | ------------------------------ #

pg.init()  # Initialize the window
pg.display.set_caption('Blitz')  # Put a title on the window

Main()

# ------------------------------------------------------------------------ #
