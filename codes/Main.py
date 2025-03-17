#!/usr/bin/env python3
# Main file ~ Handles user input & displays GameState object
############################# [ IMPORTS ] #############################

import time
import pygame as pg
from multiprocessing import Process, Queue
import AI_Core, Engine

############################# [ VARIABLES ] #############################

w = h = 512  # Width & Height of the board
movePanelW = 256  # Width of the move panel
movePanelH = h  # Height of the move panel
d = 8  # Dimension of the board (8*8)
sqSize = w // d
fps = 15  # 15fps ==> need no more
img = {}  # Dict of images
icons = {}  # Dict of icons

############################# [ FUNCTIONS ] #############################

# Function to load piece image into the board
# /!\ EXECUTE ONLY ONCE ==> too much RAM consumption
def loadImg():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]  # List of every pieces
    for p in pieces:
        img[p] = pg.transform.scale(pg.image.load(f"../images/pieces/{p}.png"), (sqSize, sqSize))  # Load each imgs with the pygame object and put it int the right size

# --------------------------------------------------
# Function to load icons of the game
def loadIcons():
    global icons
    icons = {
        "brown": pg.image.load("../images/icons/brown_icon.png"),
        "blue": pg.image.load("../images/icons/blue_icon.png"),
        "green": pg.image.load("../images/icons/green_icon.png"),
        "gray": pg.image.load("../images/icons/gray_icon.png"),
        "ai_vs_human": pg.image.load("../images/icons/bot.png"),
        "human_vs_human": pg.image.load("../images/icons/human.png"),
        "white": pg.image.load("../images/icons/bK.png"),
        "black": pg.image.load("../images/icons/wK.png"),
        "random": pg.image.load("../images/icons/random.png")
    }
    for key in icons:
        icons[key] = pg.transform.scale(icons[key], (50, 50))

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

        # Draw the animation
        screen.blit(img[move.pieceMoved], pg.Rect(col * sqSize, row * sqSize, sqSize, sqSize))
        pg.display.update()  # Update the screen
        clock.tick(60)

# --------------------------------------------------
# Function to highlight allowed moves / selected square / last move
def highlight(screen, gs, validMoves, sqSelected):
    checkHighlight = False

    # Highlight the last move
    if len(gs.moveLog) > 0:
        lastMove = gs.moveLog[-1]
        surface = pg.Surface((sqSize, sqSize))
        surface.set_alpha(100)
        surface.fill(pg.Color("yellow"))
        screen.blit(surface, (lastMove.endCol * sqSize, lastMove.endRow * sqSize))

    # Highlight inCheck king
    if gs.inCheck or gs.checkmate:
        if gs.whiteTurn:
            kRow, kCol = gs.wKLoc
        else:
            kRow, kCol = gs.bKLoc

        surface = pg.Surface((sqSize, sqSize))
        surface.set_alpha(100)
        surface.fill(pg.Color("red"))
        screen.blit(surface, (kCol * sqSize, kRow * sqSize))
        checkHighlight = True

    # Highlight the selected square
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == "w" if gs.whiteTurn else "b":  # The color is the right one
            hlSqSelected = pg.Surface((sqSize, sqSize))
            hlSqSelected.set_alpha(100)  # Transparency value : 0(invisible)-255(opaque)
            hlSqSelected.fill(pg.Color("blue"))
            # Undo the highlight if a king is in check
            if not sqSelected in [gs.wKLoc, gs.bKLoc]:
                screen.blit(hlSqSelected, (col * sqSize, row * sqSize))
            else:
                checkHighlight = False
                pass

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
    #colors = [pg.Color("white"), pg.Color("gray")]  # List of colors used on the board
    for row in range(d):
        for col in range(d):
            color = colors[(row + col) % 2]  # Make alternated color on the board
            # Draw a rectangle of the right size on the screen in the right color and place
            pg.draw.rect(screen, color, pg.Rect(col * sqSize, row * sqSize, sqSize, sqSize))
            #           screen, color, rectangle object(right x value, right y value,width,height)

# --------------------------------------------------
# Function to drwo pieces
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
        chessNot = f"{moveLog[i].getChessNot(gs)} "
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
def drawClock(screen, gs):
    pass
    # wClock = clock(600)  # 10min : decrease each sec >> no sup time
    # bClock = clock(600)

# TODO make end text with king img instead of color name
# --------------------------------------------------
# Function to draw the endgame text
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
def draw(screen, gs, validMoves, sqSelected, highlightMoves=True):
    drawBoard(screen)
    if highlightMoves:
        highlight(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoves(screen, gs)
    # TODO draw clock
    # drawClock(screen, gs, clock)

    # Dessiner la pièce soulevée si elle est sélectionnée
    if draggingPiece and draggedPiece:
        loc = pg.mouse.get_pos()
        screen.blit(img[draggedPiece], (loc[0] - sqSize // 2, loc[1] - sqSize // 2))

# --------------------------------------------------
# Draw preference menu
def showPreferencesMenu(screen):
    global icons
    font = pg.font.SysFont("Helvetica", 24)
    menu_items = [ # Check states of options
        {"text": "Select theme", "options": ["brown", "blue", "green", "gray"], "selected": "gray", "clicked": False},
        {"text": "Highlight moves", "options": [True, False], "selected": True, "clicked": False},
        {"text": "Select mode", "options": ["AI VS Human", "Human VS Human"], "selected": "AI VS Human", "clicked": False},
        {"text": "Choose side (if AI mode)", "options": ["white", "black", "random"], "selected": "white", "clicked": False,"hidden": False}, #,"hidden": False
        {"text": "AI Strength (ELO)", "options": list(range(300, 3001, 300)), "selected": 1200, "clicked": False,"hidden": False} #,"hidden": False
    ]

    running = True
    while running:
        screen.fill(pg.Color("white"))
        y_offset = 25

        for item in menu_items:
            # Hide "hidden" item in case Human VS Human is selected
            if "hidden" in item and item["hidden"]:
                continue

            text = font.render(item["text"], True, pg.Color("black"))
            screen.blit(text, (50, y_offset))

            y_offset += 40 # Stating pos of icons
            x_offset = 150

            if item["text"] == "Highlight moves":
                # Draw a switch "Highlight moves"
                switch_x, switch_y = x_offset, y_offset
                switch_width, switch_height = 60, 30
                switch_color = pg.Color("green") if item["selected"] else pg.Color("red") # color of the switch
                circle_x = switch_x + (switch_width - 20) if item["selected"] else switch_x + 5 # pos of the swtch

                pg.draw.rect(screen, switch_color, (switch_x, switch_y, switch_width, switch_height), border_radius=15)  # Draw the switch
                pg.draw.circle(screen, pg.Color("white"), (circle_x + 10, switch_y + switch_height // 2), 12)  # Draw the white circle

            elif item["text"] == "AI Strength (ELO)":
                # Draw slider for AI strength
                slider_x, slider_y = x_offset, y_offset + 10
                slider_width = 200
                pg.draw.line(screen, pg.Color("black"), (slider_x, slider_y), (slider_x + slider_width, slider_y), 4)
                knob_x = slider_x + (item["selected"] - 300) / (3000 - 300) * slider_width
                pg.draw.circle(screen, pg.Color("red"), (int(knob_x), slider_y), 10)
                elo_text = font.render(str(item["selected"]), True, pg.Color("black"))
                screen.blit(elo_text, (slider_x + slider_width + 20, slider_y - 10))

            else:
                # Draw icons for other options
                for option in item["options"]:
                    icon_key = str(option).replace(" ", "_").lower()
                    icon = icons.get(icon_key, None)

                    if icon:
                        screen.blit(icon, (x_offset, y_offset))  # Draw icon
                    else:
                        text = font.render(str(option), True, pg.Color("black")) # Write option name if icon isn't found
                        screen.blit(text, (x_offset + 10, y_offset + 15))

                    if item["selected"] == option:
                        pg.draw.rect(screen, pg.Color("red"), (x_offset, y_offset, 50, 50), 2)  # Red square to select

                    x_offset += 70  # Padding of icons

            y_offset += 60  # Padding of params

        # Event Handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                y_offset = 25 # offset of the hitboxes

                for item in menu_items:
                    y_offset += 40
                    x_offset = 150

                    if item["text"] == "Highlight moves":
                        switch_x, switch_y = x_offset, y_offset
                        switch_width, switch_height = 60, 30

                        if switch_x < x < switch_x + switch_width and switch_y < y < switch_y + switch_height:
                            item["selected"] = not item["selected"]  # Toggle switch

                    elif item["text"] == "AI Strength (ELO)":
                        # Click on slider
                        slider_x, slider_y = x_offset, y_offset + 10
                        slider_width = 200
                        if slider_x <= x <= slider_x + slider_width and slider_y - 10 <= y <= slider_y + 10:
                            new_elo = round(((x - slider_x) / slider_width) * (3000 - 300) + 300)
                            item["selected"] = min(max(new_elo, 300), 3000)  # Clamp value between 300 and 3000

                    else:
                        for option in item["options"]:
                            if x_offset < x < x_offset + 50 and y_offset < y < y_offset + 50:
                                item["selected"] = option

                                # TODO : Hide ELO and side selection if Human vs Human is selected
                                if item["text"] == "Select mode":
                                    human_vs_human = (option == "Human VS Human")
                                    for other_item in menu_items:
                                        if other_item["text"] in ["AI Strength (ELO)", "Choose side (if AI mode)"]:
                                            other_item["hidden"] = human_vs_human

                            x_offset += 70
                    y_offset += 60

            # Enter to quit menu
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    running = False

        pg.display.update()

    # Convert AI ELO to depth
    ai_depth = menu_items[-1]["selected"] // 300 if not menu_items[-1].get("hidden", False) else None

    return {item["text"]: item["selected"] for item in menu_items}, ai_depth

# --------------------------------------------------
# Main function
def run():
    pg.init()  # Initialize the pygame object
    screen = pg.display.set_mode((w + movePanelW, h))  # Define the size of the window
    pg.display.set_caption("Blitz")  # Set the title
    pg.display.set_icon(pg.image.load('../images/icons/Blitz_logo.png'))  # Set the icon
    screen.fill(pg.Color("white"))  # Make a white window (easier to see modifcations)

    clock = pg.time.Clock()  # Create an object to handles fps

    gs = Engine.GameState()  # Initialize the game
    loadImg()  # and images
    loadIcons()  # and icons

    validMoves = gs.getValidMoves()  # Get all valid moves

    sqSelected = ()  # (col,row) ==> last click
    playerClicks = []  # [(c1,r1),(c2,r2)]  ==> used to make a move

    moveDone = False  # Flag of move
    animation = False  # Flag of animation

    gameover = False  # Flag of end game
    openMode = True  # Flag to know when the opening mode ends
    AIThinking = False  # Flag for the mulitporocessing when AI try to find a move
    AIMoveFinderProcess = None  # multiprocessing informations
    undoneMove = False

    # Calling Preference Menu
    preferences, ai_depth = showPreferencesMenu(screen)
    print(preferences)
    theme = preferences["Select theme"]
    mode = preferences["Select mode"]
    side = preferences["Choose side (if AI mode)"]
    highlightMoves = preferences["Highlight moves"]

    # Apply colors
    global colors
    if theme == "brown":
        colors = [pg.Color("burlywood"), pg.Color("saddlebrown")]
    elif theme == "blue":
        colors = [pg.Color("lightblue"), pg.Color("darkblue")]
    elif theme == "green":
        colors = [pg.Color("lightgreen"), pg.Color("darkgreen")]
    else:  # gray
        colors = [pg.Color("white"), pg.Color("gray")]

    # Set playing mode
    if mode == "Human VS Human":
        p1 = True
        p2 = True
    else:  # AI VS Human
        if side == "white":
            p1 = False
            p2 = True
        elif side == "black":
            p1 = True
            p2 = False
        else:  # random
            import random
            p1, p2 = random.choice([(False, True), (True, False)])

    global draggingPiece, draggedPiece, draggedPiecePos
    draggingPiece = False # Flag to know if the current piece is dragging
    draggedPiece = None # Which piece is dragged
    draggedPiecePos = None # Pos of the draggedPiece

    run = True
    while run:
        humanTurn = (gs.whiteTurn and p1) or (not gs.whiteTurn and p2)

        for event in pg.event.get():  # Handle events of the game
            if event.type == pg.QUIT:  # click on the red cross
                run = False

            # Mouse handler - Drag & Drop
            elif event.type == pg.MOUSEBUTTONDOWN:  # mouse click
                if not gameover:
                    loc = pg.mouse.get_pos()  # (x,y) loc of the mouse
                    col = loc[0] // sqSize  # right case clicked
                    row = loc[1] // sqSize
                    if sqSelected == (row, col) or col >= 8:  # Unselect the current case if double click or click on panel
                        sqSelected = ()
                        playerClicks = []
                        if draggedPiece and draggedPiecePos: # Put back the piece if the move is invalidated
                            gs.board[draggedPiecePos[0]][draggedPiecePos[1]] = draggedPiece
                            draggedPiece = None
                            draggedPiecePos = None
                    else:
                        sqSelected = (row, col)  # Keep tracks of the click
                        playerClicks.append(sqSelected)  # Taking it as a valid click

                    if gs.board[row][col] != "  ":  # Check if clicked case is empty
                        draggingPiece = True
                        draggedPiece = gs.board[row][col]
                        draggedPiecePos = (row, col)
                        gs.board[row][col] != "  " # Erase the piece from its origin place

            # End of Drag & Drop
            elif event.type == pg.MOUSEBUTTONUP:
                if draggingPiece:
                    loc = pg.mouse.get_pos()  # Get the pos of the mouse to calculate the right case
                    col = loc[0] // sqSize
                    row = loc[1] // sqSize
                    if (row, col) != draggedPiecePos:  # Start the move
                        move = Engine.Move(draggedPiecePos, (row, col), gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveDone = True
                                animation = True
                                sqSelected = ()
                                playerClicks = []
                                break
                            else:
                                gs.board[draggedPiecePos[0]][draggedPiecePos[1]] = draggedPiece # Put back the piece if the move is invalidated
                    else:
                        gs.board[draggedPiecePos[0]][draggedPiecePos[1]] = draggedPiece # Put back the piece if the move is invalidated

                    draggingPiece = False
                    draggedPiece = None
                    draggedPiecePos = None

                elif len(playerClicks) == 2 and humanTurn:  # 2 clicks ==> move a piece from a case to an other one
                    move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)  # Create a move object

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
                    if not gameover:
                        gs.undoMove()  # Undo last move (opponent)
                        moveDone = True
                        if AIThinking:
                            AIMoveFinderProcess.terminate()
                            AIThinking = False
                        undoneMove = True

                if event.key == pg.K_ESCAPE:  # Reset gamestate on "Esc" key press
                    gs = Engine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveDone = False
                    animation = False
                    gameover = False
                    openMode = True
                    if AIThinking:
                        AIMoveFinderProcess.terminate()
                        AIThinking = False
                    undoneMove = True

        # AI move finder
        if not gameover and not humanTurn and not undoneMove:
            AI_Core.handleBook("../book.txt")  # Create an engine-readable openning book from a human-readable book
            AIMove = None
            if openMode:
                AIChoice = AI_Core.getOpenMove() if len(gs.moveLog) == 0 else AI_Core.getRightOpen(gs.moveLog, AI_Core.opennings)
                if AIChoice is not None:
                    AIMove = Engine.Move(AIChoice[0], AIChoice[1], gs.board)
                else:
                    AIMove = AI_Core.getRandomMove(validMoves)
                    openMode = False

            else:
                if not AIThinking:
                    AIThinking = True
                    returnQueue = Queue()  # Use to permit transmitting data between threads
                    AIMoveFinderProcess = Process(target=AI_Core.getBestMove,
                                                  args=(gs, validMoves, returnQueue))  # Create a parallel thread
                    AIMoveFinderProcess.start()  # Call the thread

                # Processing the multi thread
                if not AIMoveFinderProcess.is_alive():  # Check if the process been killed
                    AIMove = returnQueue.get()  # Get the move mode by the AI in the parallel thread

                if AIMove is None:  # AI Give up  => ending in any case into checkmate or stalemate
                    AIMove = AI_Core.getRandomMove(validMoves)  # Play a random move if none are good
                AIThinking = False

            gs.makeMove(AIMove, isAI=True)  # Make the move
            moveDone = True
            animation = True

        if moveDone:  # Generate a new set of valid moves only if a move is made
            if animation:
                animate(gs.moveLog[-1], screen, gs.board, clock)
                animation = False
            validMoves = gs.getValidMoves()

            moveDone = False  # Reset the flags
            undoneMove = False

        draw(screen, gs, validMoves, sqSelected, highlightMoves)  # Draw the whole game

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

    time.sleep(0.045)
    time.sleep(0.052)
    pg.quit()

############################# [ LAUNCH ] #############################

if __name__ == '__main__':
    run()
