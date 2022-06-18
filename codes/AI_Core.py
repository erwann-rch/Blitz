import random

piecesValue = {"P":1, "N":3, "B":3, "R":5, "Q":9, "K":100}
checkmate = 1000  # Scores of end games (white side => black side is the opposite)
stalemate = 500

# Function to make a random move
def getRandomMove(validMoves):
    index = random.randint(0, len(validMoves)-1)
    return validMoves[index]

# Function to determine which move is the best
def getBestMove(gs, validMoves):  # MinMax algorythm without recursion
    turnID = 1 if gs.whiteTurn else -1  # Get the turn ID to get the correct score for each side
    oppMinMaxScore = checkmate  # Minimum of the maximum score of the opponent
    bestPlayerMove = None
    random.shuffle(validMoves)  # Reorganize randomly a list to pick the first move in case of incapacity to pick the best move
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        oppMoves = gs.getValidMoves()  # Get all the opponent moves
        oppMaxScore = -checkmate  # Start very low to let the algorithm find the best score of the opponent
        for oppMove in oppMoves:
            gs.makeMove(oppMove)
            if gs.checkmate:
                oppScore = -turnID * checkmate  # Find the highest score of the opponent if checkmate
            elif gs.stalemate:
                oppScore = -turnID * stalemate  # Find the highest score of the opponent if checkmate
            else:
                oppScore = -turnID * getScores(gs.board)[0]  # Get only the board score of the opponent

            if oppScore > oppMaxScore:  # Maximize the opponent score
                oppMaxScore = oppScore
            gs.undoMove()
        # Minimize player lost by reducing at the maximum the opponent score
        if oppMaxScore < oppMinMaxScore:  # If the minimum of the max score of the opponent is greater than the max of opponent scores
            oppMinMaxScore = oppMaxScore  # Update the minimum of the max opponent score to get the lowest possible opp max score
            bestPlayerMove = playerMove  # Current playerMove is a the best move to play (2 moves ahead)
        gs.undoMove()
    return bestPlayerMove

# Function to get the actual score of the board
def getScores(board):
    boardScore = wScore = bScore = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != "  ":
                piece = board[row][col][1]
                if board[row][col][0] == "w":
                    boardScore += piecesValue[piece]  # Summing the global score of the board
                    wScore += piecesValue[piece]  # Summing the white score
                else:
                    boardScore -= piecesValue[piece]
                    bScore += piecesValue[piece]  # Summing the black score
    return boardScore, wScore, bScore
