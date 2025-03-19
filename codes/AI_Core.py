# AI Core file ~ Handle the choice of the best move depending on few algorithms

############################# [ IMPORTS ] #############################

import random, os

############################# [ VARIABLES ] #############################

# Scores of each pieces in the board
PScores = [
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
    [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
    [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
    [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
    [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
    [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
    [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
    [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
]

NScores = [
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
    [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
    [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
    [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
    [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
    [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
    [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]
]

BScores = [
    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
    [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
    [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
    [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
    [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]
]

RScores = [
    [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
    [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]
]

QScores = [
    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]
]

KScores = [
    [0.25, 0.1 , 0.1 , 0.1 , 0.1 , 0.1 , 0.1 , 0.25],
    [0.1 , 0.75, 0.0 , 0.0 , 0.0 , 0.0 , 0.75, 0.1 ],
    [0.1 , 0.0 , 0.5 , 0.0 , 0.0 , 0.5 , 0.0 , 0.1 ],
    [0.1 , 0.0 , 0.0 , 0.25, 0.25, 0.0 , 0.0 , 0.1 ],
    [0.1 , 0.0 , 0.0 , 0.25, 0.25, 0.0 , 0.0 , 0.1 ],
    [0.1 , 0.0 , 0.5 , 0.0 , 0.0 , 0.5 , 0.0 , 0.1 ],
    [0.1 , 0.75, 0.0 , 0.0 , 0.0 , 0.0 , 0.75, 0.1 ],
    [1   , 1   , 1   , 0.25, 0.25, 1   , 1   , 1   ]

]

# PScores = [
#     [1   , 1   , 1   , 1   , 1   , 1   , 1   , 1   ],
#     [0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85],
#     [0.55, 0.55, 0.65, 0.75, 0.75, 0.65, 0.55, 0.55],
#     [0.25, 0.25, 0.3 , 0.45, 0.45, 0.3 , 0.25, 0.25],
#     [0.2 , 0.2 , 0.2 , 0.4 , 0.4 , 0.2 , 0.2 , 0.2 ],
#     [0.25, 0.15, 0.1 , 0.2 , 0.2 , 0.1 , 0.15, 0.25],
#     [0.25, 0.25, 0.25, 0.35, 0.35, 0.35, 0.25, 0.25],
#     [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ]
# ]
#
# NScores = [
#     [0.0 , 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0 ],
#     [0.25, 0.5 , 0.5 , 0.5 , 0.5 , 0.5 , 0.5 , 0.25],
#     [0.25, 0.5 , 0.75, 0.75, 0.75, 0.75, 0.5 , 0.25],
#     [0.25, 0.5 , 0.75, 1   , 1   , 0.75, 0.5 , 0.25],
#     [0.25, 0.5 , 0.75, 1   , 1   , 0.75, 0.5 , 0.25],
#     [0.25, 0.5 , 0.75, 0.75, 0.75, 0.75, 0.5 , 0.25],
#     [0.25, 0.5 , 0.5 , 0.5 , 0.5 , 0.5 , 0.5 , 0.25],
#     [0.0 , 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0 ],
# ]
#
# BScores = [
#     [0.0 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.0 ],
#     [0.2 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.2 ],
#     [0.2 , 0.4 , 0.5 , 0.6 , 0.6 , 0.5 , 0.4 , 0.2 ],
#     [0.2 , 0.5 , 0.5 , 0.6 , 0.6 , 0.5 , 0.5 , 0.2 ],
#     [0.2 , 0.4 , 0.6 , 0.6 , 0.6 , 0.6 , 0.4 , 0.2 ],
#     [0.2 , 0.6 , 0.6 , 0.6 , 0.6 , 0.6 , 0.6 , 0.2 ],
#     [0.2 , 0.5 , 0.4 , 0.4 , 0.4 , 0.4 , 0.5 , 0.2 ],
#     [0.0 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.0 ]
# ]
#
# RScores = [
#     [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
#     [0.75, 1   , 1   , 1   , 1   , 1   , 1   , 0.75],
#     [0.0 , 0.25, 0.75, 0.75, 0.75, 0.75, 0.25, 0.0 ],
#     [0.0 , 0.25, 0.5 , 0.75, 0.75, 0.5 , 0.25, 0.0 ],
#     [0.0 , 0.25, 0.5 , 0.75, 0.75, 0.5 , 0.25, 0.0 ],
#     [0.0 , 0.25, 0.5 , 0.75, 0.75, 0.5 , 0.25, 0.0 ],
#     [0.0 , 0.25, 0.5 , 0.75, 0.75, 0.5 , 0.25, 0.0 ],
#     [0.25, 0.25, 0.5 , 0.5 , 0.5 , 0.5 , 0.25, 0.25]
# ]
#
# QScores = [
#     [0.25, 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.25],
#     [0.2 , 0.5 , 0.4 , 0.4 , 0.4 , 0.4 , 0.5 , 0.2 ],
#     [0.2 , 0.4 , 0.75, 1   , 1   , 0.75, 0.4 , 0.2 ],
#     [0.2 , 0.4 , 1   , 1   , 1   , 1   , 0.5 , 0.2 ],
#     [0.2 , 0.4 , 1   , 1   , 1   , 1   , 0.4 , 0.2 ],
#     [0.2 , 0.4 , 0.75, 1   , 1   , 0.75, 0.4 , 0.2 ],
#     [0.2 , 0.5 , 0.4 , 0.4 , 0.4 , 0.4 , 0.5 , 0.2 ],
#     [0.25, 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.25]
# ]


piecesValue = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 100}
piecesMapScores = {"P": PScores, "N": NScores, "B": BScores, "R": RScores, "Q": QScores, "K": KScores}

checkmate = 1000  # Scores of end games (white side => black side is the opposite)
stalemate = 0

algoDepth = 4  # Depth of the recursion

# --------------------------------------------------
# Block to make the computer-readable list of opennings
opennings = []  # List of remaining opennings
with open("../bookIO.txt", "r") as bookIO:
    opens = bookIO.readlines()
    for o in opens:
        if "\n" in o:  # Get rid of the last CR
            o = o[:-1]
        opennings.append(o.split("|"))  # Making the list of opennings

############################# [ FUNCTIONS ] #############################
# Function to write in right way the openning book
def handleBook(openBook):
    openningsList = []
    try:
        # Make the list of opennings
        with open(openBook, "r") as book:
            opens = book.readlines()
            for o in opens:
                openningsList.append(o.split())


        # Write the book in computer understandable sequences
        if not os.path.isfile("../bookIO.txt"):
            for opens in openningsList:
                with open("../bookIO.txt", "a") as book:
                    tmp = ""
                    for move in opens:  # Build a temporary str
                        rowCol = getRowCol(move)
                        tmp += f"{str(rowCol)}|"
                    tmp = tmp[:-1]  # Get rid of the last "|"
                    book.write(tmp + "\n")

    except FileNotFoundError:
        print("Book not found")
        exit()


# --------------------------------------------------
# Function to get the first random move in the opennings
def getOpenMove():
    opennings = []
    with open("../bookIO.txt", "r") as bookIO:
        opens = bookIO.readlines()
        for o in opens:
            opennings.append(o.split("|"))
        return eval(random.choice(opennings)[0])  # Convert str into tuple

# --------------------------------------------------
# Function to determine which openning is currently played
# def getRightOpen(moveLog, variants):
#     global opennings
#     #print("left :" + str(len(variants)))
#     tmpVariants = []

#     lastMove = moveLog[-1]  # Get the last move in the moveLog
#     startSq = (lastMove.startRow, lastMove.startCol)
#     endSq = (lastMove.endRow, lastMove.endCol)
#     lastMove = (startSq, endSq)  # Make a tuple of startSq and endSq of the last move

#     currentIndex = len(moveLog) - 1  # Get the index to compare the right element
#     #print(currentIndex)
#     for opens in variants:
#         if currentIndex > len(opens):
#             return
#         #print("opens "+str(len(opens)))
#         move = eval(opens[currentIndex])  # Convert the str to tuple
#         if lastMove == move:
#             tmpVariants.append(opens)  # Append the whole openning to the list of variants

#     opennings = tmpVariants  # Set the new list of remaining openings

#     if currentIndex < len(opennings):
#         return eval(random.choice(opennings)[currentIndex+1])  # Convert str into tuple
#     else:
#         return
def getRightOpen(moveLog, variants):
    global opennings
    tmpVariants = []

    if not moveLog:
        return

    lastMove = moveLog[-1]  # Get the last move in the moveLog
    startSq = (lastMove.startRow, lastMove.startCol)
    endSq = (lastMove.endRow, lastMove.endCol)
    lastMove = (startSq, endSq)  # Make a tuple of startSq and endSq of the last move

    currentIndex = len(moveLog) - 1  # Get the index to compare the right element
    # print(f"currentIndex: {currentIndex}")

    for opens in variants:
        # print(f"opens: {opens}, len(opens): {len(opens)}")
        if currentIndex >= len(opens):
            continue
        move = eval(opens[currentIndex])  # Convert the str to tuple
        if lastMove == move:
            tmpVariants.append(opens)  # Append the whole opening to the list of variants

    opennings = tmpVariants  # Set the new list of remaining openings
    # print(f"opennings: {opennings}, len(opennings): {len(opennings)}")

    if currentIndex + 1 < len(opennings):
        return eval(random.choice(opennings)[currentIndex + 1])  # Convert str into tuple
    else:
        return
# --------------------------------------------------
# Function to translate human-readable moves into computer-readable moves
def getRowCol(squares):
    #print(squares)
    startSq = squares[:2]
    endSq = squares[2:4]

    # key : value ==> chess not : index
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    # key : value ==> chess not : index
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    #g1f3 => ((row,col),(row,col))  => ((7,6),(5,5))
    return (ranksToRows[startSq[1]], filesToCols[startSq[0]]), (ranksToRows[endSq[1]], filesToCols[endSq[0]])

# --------------------------------------------------
# Function to make a random move
def getRandomMove(validMoves):
    return random.choice(validMoves)

# --------------------------------------------------
# Function to make the first recursive call
def getBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None  # Reset the previous value
    counter = 0  # Counter of recursive calling  (only for debug)

    validMoves = getOrderedMoves(gs, validMoves)  # Priority maker

    # getMinMaxMove(gs, validMoves, algoDepth, gs.whiteTurn)  # MinMax algorithm chosen
    # getNegaMaxMove(gs, validMoves, algoDepth, 1 if gs.whiteTurn else -1)  # NegaMax algorithm chosen
    getAlphaBetaMove(gs, validMoves, algoDepth, -checkmate, checkmate, 1 if gs.whiteTurn else -1)  # AlphaBeta-pruning algorithm chosen

    # print(counter)
    returnQueue.put(nextMove)  # Put the next move in the queue to travel between threads

#TODO : Set the working AlgoDepth
# def getBestMove(gs, validMoves, algoDepth, returnQueue):
#     global nextMove, counter
#     nextMove = None  # Reset the previous value
#     counter = 0  # Counter of recursive calling  (only for debug)

#     validMoves = getOrderedMoves(gs, validMoves)  # Priority maker

#     # getMinMaxMove(gs, validMoves, algoDepth, gs.whiteTurn)  # MinMax algorithm chosen
#     # getNegaMaxMove(gs, validMoves, algoDepth, 1 if gs.whiteTurn else -1)  # NegaMax algorithm chosen
#     getAlphaBetaMove(gs, validMoves, algoDepth, -checkmate, checkmate, 1 if gs.whiteTurn else -1)  # AlphaBeta-pruning algorithm chosen

#     # print(counter)
#     returnQueue.put(nextMove)  # Put the next move in the queue to travel between threads

# --------------------------------------------------
# Function to determine the best move with MinMax recursive algorithm
def getMinMaxMove(gs, validMoves, depth, whiteTurn):
    global nextMove, counter
    counter += 1

    if depth == 0:
        boardScore = getBoardScore(gs)
        return boardScore

    if whiteTurn:
        maxScore = -checkmate  # Very low value to allows find best moves of the white player
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()  # List of moves after one made
            score = getMinMaxMove(gs, nextMoves, depth - 1, not gs.whiteTurn)  # Recursive call
            if score > maxScore:  # Maximize the score
                maxScore = score
                if depth == algoDepth:  # Analyze the board to get the new best move that gonna be my best one
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = checkmate  # Very high value to allows find best moves of the black player
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()  # List of moves after one made
            score = getMinMaxMove(gs, nextMoves, depth - 1, gs.whiteTurn)  # Recursive call
            if score < minScore:  # Minimize the score
                minScore = score
                if depth == algoDepth:  # Analyze the board to get the new best move that gonna be my best one
                    nextMove = move
            gs.undoMove()
        return minScore

# --------------------------------------------------
# Function to determine the best move with NegaMax recursive algorithm
def getNegaMaxMove(gs, validMoves, depth, turnID):
    global nextMove, counter
    counter += 1
    maxScore = -checkmate

    if depth == 0:
        boardScore = getBoardScore(gs)
        return boardScore

    for move in validMoves:
        if depth == 0:
            boardScore = turnID * getBoardScore(gs)  # Negative if black
            return boardScore
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        nextMoves = getOrderedMoves(gs, nextMoves)  # Priority maker

        score = -getNegaMaxMove(gs, nextMoves, depth - 1, -turnID)  # Recursive call with switch turn by '-' because everything is reversed for the opponent
        if score > maxScore:  # Maximize the score
            maxScore = score
            if depth == algoDepth:  # Analyze the board to get the new best move that gonna be my best one
                nextMove = move
        gs.undoMove()

    return maxScore

# --------------------------------------------------
# Function to determine the best move with AlphaBeta-pruning recursive algorithm
def getAlphaBetaMove(gs, validMoves, depth, alpha, beta, turnID):
    global nextMove, counter
    counter += 1
    maxScore = -checkmate

    if depth == 0:
        return quiescenceSearch(gs, validMoves, alpha, beta)
        # boardScore = turnID * getBoardScore(gs)
        # return boardScore

    for move in validMoves:
        gs.makeMove(move, isAI=True)
        nextMoves = gs.getValidMoves()  # Get the next possible moves and put it into the recursive call
        score = -getAlphaBetaMove(gs, nextMoves, depth - 1, -beta, -alpha, -turnID)  # Recursive call with switch turn by '-' because everything is reversed for the opponent
        if score > maxScore:  # Maximizing the score
            maxScore = score
            if depth == algoDepth:  # Analyze the board to get the new best move that gonna be my best one
                nextMove = move
        gs.undoMove()

        # Make the pruning
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore

# --------------------------------------------------
# Function to make the quiescence search to limit horizon effect
def quiescenceSearch(gs, validMoves, alpha, beta):
    static_eval = getBoardScore(gs)
    if static_eval >= beta:
        return beta
    if alpha < static_eval:
        alpha = static_eval

    for move in validMoves:
        if move.pieceCaptured != "  " or move.isProm:  # If it's a tactical move
            gs.makeMove(move, isAI=True)
            nextMoves = gs.getValidMoves()
            score = -quiescenceSearch(gs, nextMoves, -beta, -alpha)
            gs.undoMove()

            if score >= beta:
                return beta  #beta cutoff
            if score > alpha:
                alpha = score
    return alpha

# --------------------------------------------------
# Function to sort the list of valid moves by worth (gains / losses), its power on the board
def getOrderedMoves(gs, validMoves):
    for move in validMoves:
        gs.makeMove(move, isAI=True)
        if gs.checkmate:
            return [move]
        gs.undoMove()

    def orderer(move):
        return moveValue(gs, move)

    orderedMoveList = sorted(
        validMoves, key=orderer, reverse=not gs.whiteTurn
    )
    return list(orderedMoveList)

# --------------------------------------------------
# Function to evaluate the weight of a move ==> Prom = ++ ; worthy capture ; position score
def moveValue(gs, move):
    if move.isProm:
        return piecesValue[move.promChoice] if gs.whiteTurn else -piecesValue[move.promChoice]

    positionScore = getBoardScore(gs)  # Get the score of the whole position
    captureScore = 0.0
    if move.pieceCaptured != "  " or move.isEp:
        captureScore = evalCapture(move)  # Evaluate the worth of a capture

    totalMoveValue = positionScore + captureScore  # Make a total score of the position after the move

    return totalMoveValue

# --------------------------------------------------
# Function to evalute the worth of a capture
def evalCapture(move):
    if move.isEp:
        return piecesValue[move.pieceMoved[1]]

    pieceCapturedValue = piecesValue[move.pieceCaptured[1]]
    pieceMovedValue = piecesValue[move.pieceMoved[1]]

    return pieceCapturedValue - pieceMovedValue  # Return positive value is the capture is favorable

# --------------------------------------------------
# Function to get the current board score of the board
def getBoardScore(gs):
    if gs.checkmate:
        if gs.whiteTurn:
            return -checkmate  # black wins
        else:
            return checkmate  # white wins

    elif gs.stalemate:
        if gs.whiteTurn:
            return -stalemate
        else:
            return stalemate

    else:
        materialScore = getMaterialScore(gs.board)[0]  # Find the current material score of the board
        return materialScore

# --------------------------------------------------
# Function to get the actual material score of the board
def getMaterialScore(board):
    materialScore = wScore = bScore = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != "  ":  # Not an empty square
                square = board[row][col]  # Get the piece on the square
                color, piece = square[0], square[1]
                if color == "w":
                    materialScore += piecesValue[piece] + piecesMapScores[piece][row][col]  # Summing the global score of the board with the score of the piece on the square
                    wScore += piecesValue[piece]  # Summing the white score
                else:
                    materialScore -= piecesValue[piece] + piecesMapScores[piece][::-1][row][col]  # Take the opposite score
                    bScore += piecesValue[piece]  # Summing the black score
    return materialScore, wScore, bScore

# TODO print each side score on the UI
# # def score(board):
#     wScore = getMaterialScore(board)[1]
#     bScore = getMaterialScore(board)[2]
#     if wScore - bScore < 0:
#         print(f"Black : +{bScore - wScore}")
#     elif wScore - bScore > 0:
#         print(f"White : +{wScore - bScore}")
