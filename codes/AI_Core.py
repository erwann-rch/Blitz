# AI Core file ~ Handle the choice of the best move depending on few algorithms

############################# [ IMPORTS ] #############################

import random

############################# [ VARIABLES ] #############################

piecesValue = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}
checkmate = 1000  # Scores of end games (white side => black side is the opposite)
stalemate = 500

algoDepth = 3  # Depth of the recursion

############################# [ FUNCTIONS ] #############################
# Function to make a random move
def getRandomMove(validMoves):
    index = random.randint(0, len(validMoves)-1)
    return validMoves[index]

# --------------------------------------------------
# Function to make the first recursive call
def getBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None  # Reset the previous value
    random.shuffle(validMoves)  # Randomize list of valid moves to avoid same starter move
    counter = 0
    # getMinMaxMove(gs, validMoves, algoDepth, gs.whiteTurn)  # MinMax algorithm chosen
    # getNegaMaxMove(gs, validMoves, algoDepth, 1 if gs.whiteTurn else -1)  # NegaMax algorithm chosen
    getAlphaBetaMove(gs, validMoves, algoDepth, -checkmate, checkmate, 1 if gs.whiteTurn else -1)  # AlphaBeta-pruning algorithm chosen
    # print(counter)
    return nextMove

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
        boardScore = turnID * getBoardScore(gs)  # Negative if black
        return boardScore

    # TODO move ordering
    for move in validMoves:
        gs.makeMove(move, isAI=True)
        nextMoves = gs.getValidMoves()  # Get the next possible moves and put it into the recursive call
        score = -getAlphaBetaMove(gs, nextMoves, depth - 1, -beta, -alpha, -turnID)  # Recursive call with switch turn by '-' because everything is reversed for the opponent
        if score > maxScore:  # Maximize the score
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
    for row in board:
        for col in row:
            if col != "  ":  # Not an empty square
                piece = col[1]  # Get the piece on the square
                if col[0] == "w":
                    materialScore += piecesValue[piece]  # Summing the global score of the board
                    wScore += piecesValue[piece]  # Summing the white score
                else:
                    materialScore -= piecesValue[piece]
                    bScore += piecesValue[piece]  # Summing the black score
    return materialScore, wScore, bScore


# def score(board):
#     wScore = getMaterialScore(board)[1]
#     bScore = getMaterialScore(board)[2]
#     if wScore - bScore < 0:
#         print(f"Black : +{bScore - wScore}")
#     elif wScore - bScore > 0:
#         print(f"White : +{wScore - bScore}")
