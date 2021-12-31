# Main file -- Handling user inputs & GameState class

# ------------------------------ | Imports | ------------------------------ #

import pygame as pg
import Engine

# ------------------------------------------------------------------------- #

# ------------------------------ | Variables | ------------------------------ #

w = h = 512  # scale of window
dim = 8  # number of cases in both Ox and Oy
sqSize = w // 8  # square size
fps = 15  # animation
img = {}  # match name of piece with its img


# --------------------------------------------------------------------------- #

# ------------------------------ | Functions | ------------------------------ #

# Loading images of the pieces /!\ ONLY ONCE
def LoadImg():
    piece = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for p in piece:
        img[p] = pg.transform.scale(pg.image.load("../images/{}.png".format(p)), (sqSize, sqSize))


# Main driver which handle updating and user input
def Main():
    screen = pg.display.set_mode((w,h))
    clock = pg.time.Clock()
    gs = Engine.GameState()
    run = True
    LoadImg()
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        Draw(screen, gs)
        clock.tick(fps)
        # screen.fill("white")
        pg.display.flip()


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
                screen.blit(img[piece], pg.Rect(col * sqSize, row * sqSize, sqSize, sqSize))


# --------------------------------------------------------------------------- #

# ------------------------------ | Launch | ------------------------------ #

pg.init()
pg.display.set_caption('Blitz')

Main()

# ------------------------------------------------------------------------ #
