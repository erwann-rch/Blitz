#!/usr/bin/env python3
# Main file ~ Handles user input & displays GameState object
############################# [ IMPORTS ] #############################

import time
import pygame as pg

import AI_Core, Engine

############################# [ VARIABLES ] #############################

w = h = 512  # Width  & Height of the board
movePanelW = 256  # Width of the move panel
movePanelH = h  # Height of the move panel
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
# Function to animate move
def animate(move, screen, board, clock):
    global colors
    deltaRow = move.endRow - move.startRow
    deltaCol = move.endCol - move.startCol
    frameOnSq = 10  # Number of frame on each squares
    frames = (abs(deltaRow) + abs(deltaCol)) * frameOnSq  # Total number of frames
    for frame in range(frames + 1):
        row, col = (move.startRow + deltaRow * frame / frames,
                    move.startCol + deltaCol * frame / frames)  # Coords = startSq + ratio
        drawBoard(screen)
        drawPieces(screen, board)

        # Erase piece from endSq => draw clear rectangle until ratio = deltaRow or deltaCol
        color = colors[(move.endRow + move.endCol) % 2]  # Get the color of the square
        endSq = pg.Rect(move.endCol * sqSize, move.endRow * sqSize, sqSize, sqSize)  # Create a rectangle object
        pg.draw.rect(screen, color, endSq)  # Draw the rectangle

        # Replace the captured piece until the end of the animation
        if move.pieceCaptured != "  ":
            screen.blit(img[move.pieceCaptured], endSq)

        # Draw the anmation
        screen.blit(img[move.pieceMoved], pg.Rect(col * sqSize, row * sqSize, sqSize, sqSize))
        pg.display.update()  # Update the screen
        clock.tick(60)


# --------------------------------------------------
# Function to highlight allowed moves / selected square / last move
def highlight(screen, gs, validMoves, sqSelected):
    # Highlight the last move
    if (len(gs.moveLog)) > 0:
        lastMove = gs.moveLog[-1]
        surface = pg.Surface((sqSize, sqSize))
        surface.set_alpha(100)
        surface.fill(pg.Color("yellow"))
        screen.blit(surface, (lastMove.endCol * sqSize, lastMove.endRow * sqSize))

    # Highlight inCheck king
    # TODO undo highlight when selected
    if gs.inCheck or gs.checkmate:
        if gs.whiteTurn:
            kRow, kCol = gs.wKLoc
        else:
            kRow, kCol = gs.bKLoc

        surface = pg.Surface((sqSize, sqSize))
        surface.set_alpha(100)
        surface.fill(pg.Color("red"))
        screen.blit(surface, (kCol * sqSize, kRow * sqSize))

    # Highlight the selected square
    # TODO highlight circles
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == "w" if gs.whiteTurn else "b":  # The color is the right one
            hlSqSelected = pg.Surface((sqSize, sqSize))
            hlSqSelected.set_alpha(100)  # Transparency value : 0(invisible)-255(opaque)
            hlSqSelected.fill(pg.Color("blue"))
            screen.blit(hlSqSelected, (col * sqSize, row * sqSize))

            hlMoves = pg.Surface((sqSize / 2, sqSize / 2))
            hlMoves.fill(pg.Color("lightgreen"))

            # Highlight each available moves
            for move in validMoves:
                if move.startRow == row and move.startCol == col:  # The move is from the selected square
                    screen.blit(hlMoves, (move.endCol * sqSize + sqSize / 4,
                                          move.endRow * sqSize + sqSize / 4))  # Highlight available move square


# --------------------------------------------------
# Secondary functions used to draw board, pieces and endgame text ==> separated to be more readable
def drawBoard(screen):
    global colors
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
# Function to draw the move log of the game
def drawMoves(screen, gs):
    # TODO clean the making of movelog
    moveLogFont = pg.font.SysFont("Helvetica", 13, True, False)  # Set the font of the movelog text
    movePanel = pg.Rect(w, 0, movePanelW, movePanelH)  # Draw the panel
    pg.draw.rect(screen, pg.Color("black"), movePanel)
    moveX = moveY = 5

    moveLog = gs.moveLog
    moveTxts = []
    for i in range(len(moveLog)):
        turn = f"{i // 2 + 1}." if i % 2 == 0 else ""  # Get the number of moves
        # Get the good check not
        # TODO make the log display complete
        # if gs.checkmate:
        #     endScore = "1-0" if not gs.whiteTurn else "0-1"  # Write the endScore
        #     chessNot = f"{moveLog[-1].getChessNot()}# {endScore}"
        # elif gs.inCheck:
        #     chessNot = f"{moveLog[-1].getChessNot()}+ "
        # elif gs.stalemate:
        #     endScore = "1/2-1/2"
        #     chessNot = f"{moveLog[-1].getChessNot()} {endScore}"
        # else:
        #     chessNot = f"{moveLog[i].getChessNot()} "
        chessNot = f"{moveLog[i].getChessNot()} "
        moveStr = turn + chessNot  # Build a str with both
        moveTxts.append(moveStr)

    moveCounter = 0
    for i in range(len(moveTxts)):
        text = moveLogFont.render(moveTxts[i], True, pg.Color("white"))  # Write the text
        loc = movePanel.move(moveX, moveY)
        screen.blit(text, loc)  # Blit text into the panel

        moveX += text.get_width()  # Spacing depending of the wight of the text
        moveCounter += 1
        if moveCounter == 6:  # Number of moves per row
            moveY += text.get_height() + 5  # Carriage Return
            moveX -= moveX - 5  # Remake the initial padding
            moveCounter = 0

# --------------------------------------------------
# Function to draw the clock on each turn
def drawClock(screen, gs, clock):
    pass


# --------------------------------------------------
# TODO make end text with king img instead of color name
def drawEndGameText(screen, text):
    font = pg.font.SysFont("Helvetica", 30, True, False)  # Set the font of the text
    txt = font.render(text, False, pg.Color("gray"))  # Write the text
    loc = pg.Rect(0, 0, w, h).move(w / 2 - txt.get_width() / 2, h / 2 - txt.get_height() / 2)  # Centering the text
    screen.blit(txt, loc)  # Shadow text

    txt = font.render(text, False, pg.Color("black"))  # Write the text
    loc = pg.Rect(0, 0, w, h).move(w / 2 - txt.get_width() / 2 + 2, h / 2 - txt.get_height() / 2 + 2)
    screen.blit(txt, loc)  # Principal text


# --------------------------------------------------
# Draw function used to draw the complete game
def draw(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlight(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoves(screen, gs)
    # TODO draw clock
    # drawClock(screen, gs, clock)


# --------------------------------------------------
# Main function
def run():
    pg.init()  # Initialize the pygame object
    screen = pg.display.set_mode((w + movePanelW, h))  # Define the size of the window
    pg.display.set_caption("Blitz")  # Set the title
    pg.display.set_icon(pg.image.load('../images/Blitz_logo.png'))  # Set the icon
    screen.fill(pg.Color("white"))  # Make a white window (easier to see modifcations)

    clock = pg.time.Clock()  # Create an object to handles fps

    gs = Engine.GameState()  # Initialize the game
    loadImg()  # and images
    validMoves = gs.getValidMoves()  # Get all valid moves

    sqSelected = ()  # (col,row) ==> last click
    playerClicks = []  # [(c1,r1),(c2,r2)]  ==> used to make a move

    moveDone = False  # Flag of move
    animation = False  # Flag of animation

    # TODO allow possibility to choose of multiplayer or not
    p1 = True  # True if human playing white
    p2 = True  # True if human playing black

    gameover = False  # Flag of end game
    run = True
    while run:
        humanTurn = (gs.whiteTurn and p1) or (not gs.whiteTurn and p2)

        for event in pg.event.get():  # Handle events of the game
            if event.type == pg.QUIT:  # click on the red cross
                run = False

            # Mouse handler
            elif event.type == pg.MOUSEBUTTONDOWN:  # mouse click
                if not gameover and humanTurn:
                    loc = pg.mouse.get_pos()  # (x,y) loc of the mouse
                    col = loc[0] // sqSize  # right case clicked
                    row = loc[1] // sqSize
                    if sqSelected == (row, col) or col >= 8:  # Unselect the current case if double click or click on panel
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)  # Keep tracks of the click
                        playerClicks.append(sqSelected)  # Taking it as a valid click

                    if len(playerClicks) == 2:  # 2 clicks ==> move a piece from a case to an other one

                        # Create a move object
                        if (gs.whiteTurn and playerClicks[1][1] == 0) or (not gs.whiteTurn and playerClicks[1][
                            1] == 7):  # Make sure the move is ending on the last rank
                            if gs.board[playerClicks[0][0]][playerClicks[0][1]][
                                1] == "P":  # Make sure the piece move is a pawn
                                move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                                # TODO prom option
                                # move = Engine.Move(playerClicks[0], playerClicks[1], gs.board, isProm=True)  # Last rank + P = prom

                            else:  # Not a pawn
                                move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        else:  # Not on last rank
                            move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                # Choice of the pawn prom after the move done
                                gs.makeMove(validMoves[i])  # Make the move
                                moveDone = True
                                animation = True

                                # Clear the click record of the turn
                                sqSelected = ()
                                playerClicks = []

                        if not moveDone:  # Fix the click wasting
                            playerClicks = [sqSelected]  # Pop the first click and only keep the last one

            # Key handler
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_u:  # Undo on "U" key press
                    if not gameover and humanTurn:
                        gs.undoMove()  # Undo last move (opponent)
                        gs.undoMove()  # Undo previous move (player)
                        moveDone = True

                if event.key == pg.K_ESCAPE:  # Reset on "Esc" key press
                    gs = Engine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveDone = False
                    animation = False
                    gameover = False

        # AI move finder
        if not gameover and not humanTurn:
            AIMove = AI_Core.getBestMove(gs, validMoves)  # Find the best AI move depending on the chosen algorithm
            if AIMove is None:  # AI Give up  => ending in any case into checkmate or stalemate
                AIMove = AI_Core.getRandomMove(validMoves)  # Play a random move is none are good

            gs.makeMove(AIMove, isAI=True)  # Make the move
            moveDone = True
            animation = True

        if moveDone:  # Generate a new set of valid moves only if a move is made
            # print(gs.currentCastles.wQs, gs.currentCastles.wKs, gs.currentCastles.bQs, gs.currentCastles.bKs)
            # print(gs.castlesLog)
            if animation:
                animate(gs.moveLog[-1], screen, gs.board, clock)
                animation = False
            validMoves = gs.getValidMoves()
            # print(len(validMoves))

            # # Get the good check not
            # if len(gs.moveLog) > 0:
            #     if gs.checkmate:
            #         print(gs.moveLog[-1].getChessNot() + "#")
            #     elif gs.inCheck:
            #         print(gs.moveLog[-1].getChessNot() + "+")
            #     else:
            #         print(gs.moveLog[-1].getChessNot())

            moveDone = False  # Reset the flags

        draw(screen, gs, validMoves, sqSelected)  # Draw the whole game

        # Write the end game
        if gs.checkmate or gs.stalemate:
            gameover = True
            if gs.stalemate:
                txt = "Stalemate ! Draw : 1/2 - 1/2"
            else:
                txt = "Checkmate ! White wins : 1 - 0" if not gs.whiteTurn else "Checkmate ! Black wins : 0 - 1"

            drawEndGameText(screen, txt)

        clock.tick(fps)  # Makes the clock ticking at fps frames rate
        pg.display.update()  # Update the board at every tick
        # if not humanTurn:  # Slow the speed of the game
        #    time.sleep(1)

    time.sleep(0.045)
    time.sleep(0.052)
    pg.quit()


############################# [ LAUNCH ] #############################

if __name__ == '__main__':
    run()
