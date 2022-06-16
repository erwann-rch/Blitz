#!/usr/bin/env python3
# Main file ~ Handles user input & displays GameState object
############################# [ IMPORTS ] #############################

import pygame as pg
import Engine

############################# [ VARIABLES ] #############################

w = h = 512  # Width  & Height of the board
d = 8  # Dimension of the board (8*8)
sqSize = w // d
fps = 15  # 15fps ==> need no more
img = {}  # Dict of images


############################# [ FUNCTIONS ] #############################

# Function to load images into the board
# /!\ EXECUTE ONLY ONCE ==> too much RAM consumption
def loadImg():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]  # List of every pieces
    for p in pieces:
        img[p] = pg.transform.scale(pg.image.load(f"../images/{p}.png"), (sqSize, sqSize))  # Load each imgs with the pygame object and put it int the right size


# --------------------------------------------------
# Draw function used to draw the complete game
def draw(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


# --------------------------------------------------
# Secondary functions used to draw board and pieces ==> separated to be more readable
def drawBoard(screen):
    colors = [pg.Color("white"), pg.Color("gray")]  # List of colors used on the board
    for row in range(d):
        for col in range(d):
            color = colors[(row + col) % 2]  # Make alternated color on the board
            # Draw a rectangle of the right size on the screen in the right color and place
            pg.draw.rect(screen, color, pg.Rect(col * sqSize, row * sqSize, sqSize, sqSize))
            #           screen, color, rectangle object(right x value, right y value,width,height)


# --------------------------------------------------
def drawPieces(screen, board):
    for row in range(d):
        for col in range(d):
            piece = board[row][col]  # Assign a piece for each case
            if piece != "  ":  # Not empty ones
                # Overlay img of the piece and the board drew
                screen.blit(img[piece], pg.Rect(col * sqSize, row * sqSize, sqSize, sqSize))


# --------------------------------------------------
# Main function
def run():
    pg.init()  # Initialize the pygame object
    screen = pg.display.set_mode((w, h))  # Define the size of the window
    pg.display.set_caption("Blitz")  # Set the title
    pg.display.set_icon(pg.image.load('../images/Blitz_logo.png'))  # Set the icon
    screen.fill(pg.Color("white"))  # Make a white window (easier to see modifications)

    clock = pg.time.Clock()  # Create an object to handles fps

    gs = Engine.GameState()  # Initialize the game
    loadImg()  # and images
    validMoves = gs.getValidMoves()  # Get all valid moves
    moveDone = False  # Flag
    sqSelected = ()  # (col,row) ==> last click
    playerClicks = []  # [(c1,r1),(c2,r2)]  ==> used to make a move
    run = True
    while run:
        for event in pg.event.get():  # Handle events of the game
            if event.type == pg.QUIT:  # click on the red cross
                pg.quit()
                run = False

            # Mouse handler
            elif event.type == pg.MOUSEBUTTONDOWN:  # mouse click
                loc = pg.mouse.get_pos()  # (x,y) loc of the mouse
                col = loc[0] // sqSize  # right case clicked
                row = loc[1] // sqSize
                color = "w" if gs.whiteTurn else "b"
                if sqSelected == (row, col):  # Unselect the current case if double click
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)  # Keep tracks of the click
                    playerClicks.append(sqSelected)  # Taking it as a valid click

                if len(playerClicks) == 2:  # 2 clicks ==> move a piece from a case to an other one
                    move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)  # Create a move object
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            # Choice of the pawn prom after the move done
                            gs.makeMove(validMoves[i])  # Make the move
                            print(validMoves[i].getChessNot())
                            moveDone = True

                            # Clear the click record of the turn
                            sqSelected = ()
                            playerClicks = []

                    if not moveDone:  # Fix the click wasting
                        playerClicks = [sqSelected]  # Pop the first click and only keep the last one

            # Key handler
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_u:  # Undo on "U" key press
                    gs.undoMove()
                    moveDone = True

        if moveDone:  # Generate a new set of valid moves only if a move is made
            validMoves = gs.getValidMoves()
            print(len(validMoves))
            moveDone = False  # Reset the flag

        draw(screen, gs)  # Draw the whole game
        clock.tick(fps)  # Makes the clock ticking at fps frames rate
        pg.display.update()  # Update the board at every tick


############################# [ LAUNCH ] #############################

run()
