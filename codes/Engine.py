# Engine file ~ Creates GameState object and handles scores, moves & logs

############################# [ CLASSES ] #############################
# Class to create game-style object
class GameState():

    def __init__(self):
        # TODO flip the board if multiplayer
        # self.board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        #     ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        #     ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        #     ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        #     ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        #     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        # ]
        self.board = [
            ["bR", "  ", "  ", "  ", "bK", "  ", "  ", "wK"],
            ["bP", "wP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "bQ"],
            ["bQ", "  ", "  ", "  ", "  ", "wP", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["wP", "bP", "wP", "wP", "wP", "wP", "bP", "wP"],
            ["wR", "  ", "  ", "  ", "  ", "  ", "  ", "wR"]
        ]

        self.whiteTurn = True  # Define the turn
        self.flip = False  # Flip the board if multiplayer
        self.board = self.board[::-1] if self.flip and not self.whiteTurn else self.board

        self.moveLog = []  # Define the list of played moves
        self.pieceMoves = {"P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                           "B": self.getBishopMoves, "K": self.getKingMoves,
                           "Q": self.getQueenMoves}  # Define the use of each move function
        # Endgame flags
        self.checkmate = False
        self.stalemate = False

        # Keep track of kings locations
        self.wKLoc = (7, 4)
        self.bKLoc = (0, 4)

        # Defines variables to get list of legal moves
        self.pinnedPieces = []  # List of pinned piece for each move
        self.currentChecks = []  # List of threatening pieces for each move
        self.inCheck = False  # Flag to know if there is a check

        # Keep track of en-passant variables
        self.epPossible = ()  # Coords of the possible en-passant
        self.epLog = [self.epPossible]

        # Keep track of castling variables
        self.currentCastles = CastleRights(True, True, True, True)  # All the castles are allowed in starting game
        self.castlesLog = [self.currentCastles]
        #self.castlesLog = [CastleRights(self.currentCastles.wQs, self.currentCastles.wKs, self.currentCastles.bQs, self.currentCastles.bKs)]

        # Variables to improve AI algorithm
        self.protects = []  # How many pieces a piece protects on each moves
        self.threats = []  # How many pieces a piece threats on each moves
        self.allowedSq = []  # How many squares a piece has on each moves

    # Function to make moves and captures
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "  "  # Leave a blank behind the piece moved
        self.board[move.endRow][move.endCol] = move.pieceMoved  # Move the piece to its ending square
        self.moveLog.append(move)
        self.whiteTurn = not self.whiteTurn  # Switch turn

        # Record king movements
        if move.pieceMoved == "wK":
            self.wKLoc = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.bKLoc = (move.endRow, move.endCol)

        # Handling pawn promotion
        if move.isProm:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + move.promChoice  # Changing the piece type into choice

        # Handling en-passant
        if move.isEp:
            self.board[move.startRow][move.endCol] = "  "  # Capturing the piece at startRow but enCol

        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:  # Only if piece moved is a pawn and the absolute value of the difference between start and end Row is 2
            self.epPossible = ((move.startRow + move.endRow)/2, move.endCol)  # The free square is between start and endRow
        else:
            self.epPossible = ()  # Reset if any other move is made

        self.epLog.append(self.epPossible)

        # Handling castling moves
        if move.isCastle:
            if 0 <= move.endCol - 2 <= 7 and 0 <= move.endCol + 1 <= 7:
                if move.endCol - move.startCol == 2:  # King side
                    self.board[move.endRow][move.endCol - 1] = "wR" if move.pieceMoved[0] == "w" else "bR"  # Move the rook too
                    self.board[move.endRow][move.endCol + 1] = "  "  # Leave a blank at the original rook place
                else:  # Queen side
                    self.board[move.endRow][move.endCol + 1] = "wR" if move.pieceMoved[0] == "w" else "bR"
                    self.board[move.endRow][move.endCol - 2] = "  "

        self.updateCastle(move)  # Update castle rights if rook or king is moved

        # Handling the 3 identical move stalemate
        if len(self.moveLog) >= 4:
            repetitions = 0  # Number of repetitions of the move
            for i in range(4):
                for move in self.moveLog[-4:]:
                    tmp = self.moveLog[i-4]  # Ally move
                    tmp1 = self.moveLog[i-3]  # Opponent move
                    # Check if the two last moves of each player are the same
                    if (move.startRow == tmp.startRow and move.endRow == tmp.endRow) and (
                            move.startRow == tmp1.startRow and move.endRow == tmp1.endRow):
                        repetitions += 1
                        if repetitions > 2:
                            self.stalemate = True

        # Handling the insufficient material stalemate
        count = 0  # Number of pieces still on the board
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col][1] != "K":  # Not a king
                    if self.board[row][col] != "  ":  # Not a empty space
                        count += 1
                        break
        if count < 1:
            self.stalemate = True

    # Function to undo the last move
    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved  # Replace the piece moved to its original square
            self.board[move.endRow][move.endCol] = move.pieceCaptured  # Replace the piece captured
            self.whiteTurn = not self.whiteTurn
            # Record king movements
            if move.pieceMoved == "wK":
                self.wKLoc = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.bKLoc = (move.startRow, move.startCol)

            # Undo ep
            self.epLog.pop()
            self.epPossible = self.epLog[-1]  # Reset the ep possible move
            if move.isEp:
                self.board[move.endRow][move.endCol] = "  "  # Leave a blank in the square behind the piece captured
                self.board[move.startRow][move.endCol] = move.epPieceCaptured  # Put back the captured pawn

            # Undo castle rights
            self.castlesLog.pop()  # Get rid of the current rights
            self.currentCastles = self.castlesLog[-1]  # Reset rights at last ones
            if move.isCastle:
                if 0 <= move.endCol - 2 <= 7 and 0 <= move.endCol + 1 <= 7:
                    if move.endCol - move.startCol == 2:  # King side
                        self.board[move.endRow][move.endCol - 1] = "  "  # Leave a blank to the last pos of the rook
                        self.board[move.endRow][move.endCol + 1] = "wR" if move.pieceMoved[0] == "w" else "bR"  # Put it back
                    else:
                        self.board[move.endRow][move.endCol + 1] = "  "
                        self.board[move.endRow][move.endCol - 2] = "wR" if move.pieceMoved[0] == "w" else "bR"

            # Undo the end game
            self.checkmate = False
            self.stalemate = False

    # Function to get all possible moves
    def getAvailableMoves(self):
        availableMoveList = []  # all the available moves on the turn
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != "  ":  # Check if the square isn't empty
                    color = self.board[row][col][0]  # Get the color of the piece
                    if (color == "w" and self.whiteTurn) or (color == "b" and not self.whiteTurn):
                        piece = self.board[row][col][1]  # Get the piece
                        self.pieceMoves[piece](row, col, availableMoveList)  # Calling each move function with only one line
        return availableMoveList

    # Function to get all legal moves (without open checks)
    def getValidMoves(self):

        tmpEp = self.epPossible  # Save the epPossible to avoid bugs from makemove
        #tmpCr = self.currentCastles  # Save the Castle rights
        tmpCr = CastleRights(self.currentCastles.wQs, self.currentCastles.wKs, self.currentCastles.bQs, self.currentCastles.bKs)

        validMovesList = []
        self.inCheck, self.pinnedPieces, self.currentChecks = self.getPinsAndChecks()  # Get the variable to restrain

        # Get the position of the king
        kingRow, kingCol = self.wKLoc if self.whiteTurn else self.bKLoc

        if self.inCheck:
            if len(self.currentChecks) == 1:  # 1 check : block or move
                validMovesList = self.getAvailableMoves()  # Get all the available moves to remove ones who don't block
                if self.whiteTurn:
                    self.getCastle(self.wKLoc[0], self.wKLoc[1], validMovesList)  # Get castling white moves
                else:
                    self.getCastle(self.bKLoc[0], self.bKLoc[1], validMovesList)  # Get castling black moves

                checkCoords = self.currentChecks[0]
                checkRow, checkCol = checkCoords[0], checkCoords[1]  # Get coords of the threatening piece
                threateningPiece = self.board[checkRow][checkCol]  # Get the piece
                validSq = []  # List of squares allowed
                if threateningPiece[1] == "N":  # Attacked by a Knight
                    validSq = [(checkRow, checkCol)]  # Can capture it
                else:
                    for i in range(1, 8):
                        sqValid = (kingRow + checkCoords[2][0] * i, kingCol + checkCoords[2][1] * i)  # (kingRow+dirr[0]*i,kingCol+dirr[1]*i)
                        validSq.append(sqValid)  # Add it to the list of allowed squares
                        if sqValid[0] == checkRow and sqValid[1] == checkCol:  # break if for loop reach the piece of the attacker
                            break
                # Delete any moves that doesn't block check (except king moves)
                for i in range(len(validMovesList) - 1, -1, -1):  # Go through backward list to avoid weird bug of duplicated occurrence due to new indexes
                    if validMovesList[i].pieceMoved[1] != 'K':  # Move king allowed
                        if not (validMovesList[i].endRow, validMovesList[i].endCol) in validSq:  # Move that doesn't block check
                            validMovesList.remove(validMovesList[i])  # Delete it from the list of allowed moves

            else:  # double check : king moves
                self.getKingMoves(kingRow, kingCol, validMovesList)

            if len(validMovesList) == 0:
                self.checkmate = True

        else:  # No check : all available moves are legal
            validMovesList = self.getAvailableMoves()  # All moves
            if self.whiteTurn:
                self.getCastle(self.wKLoc[0], self.wKLoc[1], validMovesList)  # And castling white moves
            else:
                self.getCastle(self.bKLoc[0], self.bKLoc[1], validMovesList)  # And castling black moves

            if len(validMovesList) == 0:
                self.stalemate = True

        self.epPossible = tmpEp  # Reset it
        self.currentCastles = tmpCr  # Reset it
        return validMovesList

    # Function to get pawn available moves
    def getPawnMoves(self, row, col, moveList):
        isPinned = False  # Test if the pawn is pinned
        pinDirr = ()  # If yes : from where
        for i in range(len(self.pinnedPieces) - 1, -1, -1):  # syntax : range(start,stop,step)
            if self.pinnedPieces[i][0] == row and self.pinnedPieces[i][1] == col:  # Test if the current pawn is pinned
                isPinned = True
                pinDirr = (self.pinnedPieces[i][2][0], self.pinnedPieces[i][2][1])  # Set the direction of the pin
                self.pinnedPieces.remove(self.pinnedPieces[i])
                break

        if self.whiteTurn:
            kingRow, kingCol = self.wKLoc
            if self.board[row - 1][col] == "  ":  # Append this if the front square is empty
                if not isPinned or pinDirr == (-1, 0):  # No blocking pin (dirr = up)
                    moveList.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "  ":  # Append this only if the pawn is on row 2 and the ending square is empty
                        moveList.append(Move((row, col), (row - 2, col), self.board))

            if col > 0 and self.board[row - 1][col - 1][0] == "b":  # Left capture on enemy piece
                if not isPinned or pinDirr == (-1, -1):  # No blocking pin (dirr = up-left)
                    moveList.append(Move((row, col), (row - 1, col - 1), self.board))
            elif col > 0 and self.board[row - 1][col - 1] == "  ":
                if (row - 1, col - 1) == self.epPossible:
                    threat = block = False
                    if kingRow == row:
                        if kingCol < col:  # king at the pawn left
                            insideRange = range(kingCol + 1, col - 1)  # Between king's right side and pawn's left side
                            outsideRange = range(col + 1, len(self.board[row]))  # Between pawn's right side and border
                        else:  # king at the pawn right
                            insideRange = range(kingCol - 1, col, -1)  # Between king's left side and pawn's right side
                            outsideRange = range(col - 2, -1, -1)  # Between enemy pawn's left side and king's right side

                        for i in insideRange:
                            if self.board[row][i] != "  ":  # Some other piece than both e.p. pawns blocks the check
                                block = True
                        for i in outsideRange:
                            piece = self.board[row][i]
                            enemy = "w" if not self.whiteTurn else "b"
                            if piece[0] == enemy and piece[1] in ["R", "Q"]:  # Piece able to attack the king
                                threat = True  # Not legal e.p. if there is no blocking piece
                            elif piece != "  ":
                                block = True  # Anything else block the check so e.p. is legal

                    if not threat or block:  # Append if threat + block or block or none
                        moveList.append(Move((row, col), (row - 1, col - 1), self.board, isEp=True))  # Add the en-passant to the list of valid moves

            if col < 7 and self.board[row - 1][col + 1][0] == "b":  # Right capture
                if not isPinned or pinDirr == (-1, 1):  # No blocking pinned (dirr = up-right)
                    moveList.append(Move((row, col), (row - 1, col + 1), self.board))
            elif col < 7 and self.board[row - 1][col + 1] == "  ":
                if (row - 1, col + 1) == self.epPossible:  # Add the en-passant to the list of valid moves
                    threat = block = False
                    if kingRow == row:
                        if kingCol < col:  # king at the pawn left
                            insideRange = range(kingCol + 1, col)  # Between king's right side and pawn's left side
                            outsideRange = range(col + 2, len(self.board[row]))  # Between enemy pawn's right side and border
                        else:  # king at the pawn left
                            insideRange = range(kingCol - 1, col + 1, -1)  # Between king's left side and pawn's right side
                            outsideRange = range(col - 1, -1, -1)  # Between pawn's left side and king's right side

                        for i in insideRange:
                            if self.board[row][i] != "  ":  # Some other piece than both e.p. pawns blocks the check
                                block = True
                        for i in outsideRange:
                            piece = self.board[row][i]
                            enemy = "w" if not self.whiteTurn else "b"
                            if piece[0] == enemy and piece[1] in ["R", "Q"]:  # Piece able to attack the king
                                threat = True  # Not legal e.p. if there is no blocking piece
                            elif piece != "  ":
                                block = True  # Anything else block the check so e.p. is legal

                    if not threat or block:  # Append if threat + block or block or none
                        moveList.append(Move((row, col), (row - 1, col + 1), self.board, isEp=True))  # Add the en-passant to the list of valid moves

        else:  # Same but with back side values
            kingRow, kingCol = self.bKLoc
            if self.board[row + 1][col] == "  ":
                if not isPinned or pinDirr == (1, 0):
                    moveList.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "  ":
                        moveList.append(Move((row, col), (row + 2, col), self.board))

            if col > 0 and self.board[row + 1][col - 1][0] == "w":
                if not isPinned or pinDirr == (1, -1):
                    moveList.append(Move((row, col), (row + 1, col - 1), self.board))
            elif col > 0 and self.board[row + 1][col - 1] == "  ":
                if (row + 1, col - 1) == self.epPossible:
                    threat = block = False
                    if kingRow == row:
                        if kingCol < col:  # king at the pawn left
                            insideRange = range(kingCol + 1, col - 1)  # Between king's right side and pawn's left side
                            outsideRange = range(col + 1, len(self.board[row]))  # Between pawn's right side and border
                        else:  # king at the pawn right
                            insideRange = range(kingCol - 1, col, -1)  # Between king's left side and pawn's right side
                            outsideRange = range(col - 2, -1,
                                                 -1)  # Between enemy pawn's left side and king's right side

                        for i in insideRange:
                            if self.board[row][i] != "  ":  # Some other piece than both e.p. pawns blocks the check
                                block = True
                        for i in outsideRange:
                            piece = self.board[row][i]
                            enemy = "w" if not self.whiteTurn else "b"
                            if piece[0] == enemy and piece[1] in ["R", "Q"]:  # Piece able to attack the king
                                threat = True  # Not legal e.p. if there is no blocking piece
                            elif piece != "  ":
                                block = True  # Anything else block the check so e.p. is legal

                    if not threat or block:  # Append if threat + block or block or none
                        moveList.append(Move((row, col), (row + 1, col - 1), self.board, isEp=True))

            if col < 7 and self.board[row + 1][col + 1][0] == "w":
                if not isPinned or pinDirr == (1, 1):
                    moveList.append(Move((row, col), (row + 1, col + 1), self.board))
            elif col < 7 and self.board[row + 1][col + 1] == "  ":
                if (row + 1, col + 1) == self.epPossible:
                    if (row - 1, col + 1) == self.epPossible:  # Add the en-passant to the list of valid moves
                        threat = block = False
                        if kingRow == row:
                            if kingCol < col:  # king at the pawn left
                                insideRange = range(kingCol + 1, col)  # Between king's right side and pawn's left side
                                outsideRange = range(col + 2,
                                                     len(self.board[row]))  # Between enemy pawn's right side and border
                            else:  # king at the pawn left
                                insideRange = range(kingCol - 1, col + 1,
                                                    -1)  # Between king's left side and pawn's right side
                                outsideRange = range(col - 1, -1, -1)  # Between pawn's left side and king's right side

                            for i in insideRange:
                                if self.board[row][i] != "  ":  # Some other piece than both e.p. pawns blocks the check
                                    block = True
                            for i in outsideRange:
                                piece = self.board[row][i]
                                enemy = "w" if not self.whiteTurn else "b"
                                if piece[0] == enemy and piece[1] in ["R", "Q"]:  # Piece able to attack the king
                                    threat = True  # Not legal e.p. if there is no blocking piece
                                elif piece != "  ":
                                    block = True  # Anything else block the check so e.p. is legal

                        if not threat or block:  # Append if threat + block or block or none
                            moveList.append(Move((row, col), (row + 1, col + 1), self.board, isEp=True))  # Add the en-passant to the list of valid moves

    # Function to get rook available moves
    def getRookMoves(self, row, col, moveList):
        isPinned = False
        pinDirr = ()
        for i in range(len(self.pinnedPieces) - 1, -1, -1):
            if self.pinnedPieces[i][0] == row and self.pinnedPieces[i][1] == col:
                isPinned = True
                pinDirr = (self.pinnedPieces[i][2][0], self.pinnedPieces[i][2][1])
                if self.board[row][col][1] != "Q":  # Don't remove if it's a queen ==> queen generate both rook and bishop moves
                    self.pinnedPieces.remove(self.pinnedPieces[i])
                break

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))  # List of available directions for the rook
        #             down,up,left,right
        enemy = "b" if self.whiteTurn else "w"  # Choose what is the enemy color
        for dirr in directions:
            for i in range(1, 8):
                endRow = row + dirr[0] * i
                endCol = col + dirr[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On the board
                    if not isPinned or pinDirr == dirr or pinDirr == (-dirr[0], -dirr[1]):  # Direction or its opposite to allow moves to and away of the pin
                        endPiece = self.board[endRow][endCol]  # Get the end piece to know if the move is valid or not
                        if endPiece == "  ":  # valid move : empty space
                            moveList.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemy:  # valid move : enemy piece
                            moveList.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else:  # invalid move : ally piece
                            break
                else:  # Outside the board
                    break

    # Function to get bishop available moves
    def getBishopMoves(self, row, col, moveList):
        isPinned = False
        pinDirr = ()
        for i in range(len(self.pinnedPieces) - 1, -1, -1):
            if self.pinnedPieces[i][0] == row and self.pinnedPieces[i][1] == col:
                isPinned = True
                pinDirr = (self.pinnedPieces[i][2][0], self.pinnedPieces[i][2][1])
                self.pinnedPieces.remove(self.pinnedPieces[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # List of available directions for the bishop : (row,col)
        #             down-left,down-right,up-left,up-right
        enemy = "b" if self.whiteTurn else "w"  # Choose what is the enemy color
        for dirr in directions:
            for i in range(1, 8):
                endRow = row + dirr[0] * i
                endCol = col + dirr[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On the board
                    if not isPinned or pinDirr == dirr or pinDirr == (-dirr[0], -dirr[1]):
                        endPiece = self.board[endRow][endCol]  # Get the end piece to know if the move is valid or not
                        if endPiece == "  ":  # valid move : empty space
                            moveList.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemy:  # valid move : enemy piece
                            moveList.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else:  # invalid move : friendly piece
                            break
                else:  # Outside the board
                    break

    # Function to get knight available moves
    def getKnightMoves(self, row, col, moveList):
        isPinned = False
        for i in range(len(self.pinnedPieces) - 1, -1, -1):
            if self.pinnedPieces[i][0] == row and self.pinnedPieces[i][1] == col:
                isPinned = True
                self.pinnedPieces.remove(self.pinnedPieces[i])
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))  # List of available directions for the knight : (row,col)
        #             SSW,SSE,SW,SE,NW,NE,NNW,NNE
        ally = "w" if self.whiteTurn else "b"  # Choose what is the ally color
        for dirr in directions:
            endRow = row + dirr[0]
            endCol = col + dirr[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not isPinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != ally:  # Not an ally piece (empty or enemy piece)
                        moveList.append(Move((row, col), (endRow, endCol), self.board))

    # Function to get king available moves
    def getKingMoves(self, row, col, moveList):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))  # List of available directions for the king : (row,col)
        #             down-left,down,down-right,left,right,up-left,up,up-right
        ally = "w" if self.whiteTurn else "b"  # Choose what is the ally color
        for dirr in directions:
            endRow = row + dirr[0]
            endCol = col + dirr[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:  # Not an ally : empty or enemy
                    # Put the king on each squares around to check if there are not available
                    if self.whiteTurn:
                        self.wKLoc = (endRow, endCol)
                    else:
                        self.bKLoc = (endRow, endCol)

                    inCheck = self.getPinsAndChecks()[0]  # Get the checks for each square

                    if not inCheck:
                        moveList.append(Move((row, col), (endRow, endCol), self.board))  # If free ==> legal move

                    # Put king to its original location.
                    if self.whiteTurn:
                        self.wKLoc = (row, col)
                    else:
                        self.bKLoc = (row, col)

    # Function to get queen available moves
    def getQueenMoves(self, row, col, moveList):  # Queen = Bishop + Rook
        self.getRookMoves(row, col, moveList)
        self.getBishopMoves(row, col, moveList)

    # Function to determine if a square is attacked
    def isAttacked(self, row, col):
        self.whiteTurn = not self.whiteTurn  # Switch turn
        oppMoves = self.getAvailableMoves()  # Get all the opponents moves
        self.whiteTurn = not self.whiteTurn  # Switch back to avoid turns problems
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:  # Square attacked
                return True
        return False

    # Function to get the list of pins and checks to restrain available moves
    def getPinsAndChecks(self):
        pins = []  # Square where the allied pinned piece is and direction pinned from
        checks = []  # Squares from where enemy is applying a check
        inCheck = False

        # Get king position
        kingRow, kingCol = self.wKLoc if self.whiteTurn else self.bKLoc

        # Get colors of the turn
        ally = "w" if self.whiteTurn else "b"
        enemy = "b" if self.whiteTurn else "w"

        # Check for checks and pins from king pos
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            dirr = directions[j]
            possiblePin = ()  # Reset possible pins
            for i in range(1, 8):
                endRow = kingRow + dirr[0] * i
                endCol = kingCol + dirr[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ally and endPiece[1] != "K":  # Check for pin and avoid 'phantom king' due to the calling in getKingMoves()
                        if possiblePin == ():  # 1st pin
                            possiblePin = (endRow, endCol, dirr)  # Add it to pinned one
                        else:  # 2nd pin ==> no check or pin possible
                            break
                    elif endPiece[0] == enemy:  # Check for checks
                        piece = endPiece[1]

                        # each scenarios of check :
                        #     - rook on orthogonal dirs
                        #     - bishop on diagonal dirs
                        #     - pawn on next down left or right square if it's black turn
                        #     - pawn on next up left or right square if it's white turn
                        #     - queen on any direction
                        #     - king on any next square

                        if (0 <= j <= 3 and piece == 'R') or (
                            4 <= j <= 7 and piece == 'B') or (
                            i == 1 and piece == 'P' and (
                            (enemy == 'w' and 6 <= j <= 7) or (enemy == 'b' and 4 <= j <= 5))) or (
                            piece == 'Q') or (i == 1 and piece == 'K'):
                            if possiblePin == ():  # No pin ==> check
                                inCheck = True
                                checks.append((endRow, endCol, dirr))
                                break
                            else:  # Piece pinned ==> no check
                                pins.append(possiblePin)
                                break
                        else:  # No check
                            break
                else:  # Outside the board
                    break

        # check for knight checks
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for dirr in directions:
            endRow = kingRow + dirr[0]
            endCol = kingCol + dirr[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemy and endPiece[1] == 'N':  # Enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, dirr))
        return inCheck, pins, checks

    # Function to update castling rights
    def updateCastle(self, move):
        tmpCastle = CastleRights(self.currentCastles.wQs, self.currentCastles.wKs, self.currentCastles.bQs, self.currentCastles.bKs)  # Take the current rights as a base to new rights
        if move.pieceMoved[1] in ["K", "R"]:
            if move.pieceMoved[1] == "K":  # King move
                if move.pieceMoved[0] == "w":  # No white castles allowed anymore
                    tmpCastle.wQs = False
                    tmpCastle.wKs = False
                else:  # No black castles allowed anymore
                    tmpCastle.bQs = False
                    tmpCastle.bKs = False

            else:  # Rook move
                if move.pieceMoved[0] == "w":
                    if move.startCol == 0:  # Left white rook
                        tmpCastle.wQs = False
                    if move.startCol == 7:  # Right white rook
                        tmpCastle.wKs = False
                else:
                    if move.startCol == 0:  # Left black rook
                        tmpCastle.bQs = False
                    if move.startCol == 7:  # Right black rook
                        tmpCastle.bKs = False

        # Rook captured
        if move.pieceCaptured[1] == "R":
            if move.pieceCaptured[0] == "w":
                if move.endCol == 7:
                    tmpCastle.wKs = False
                elif move.endCol == 0:
                    tmpCastle.wQs = False
            else:
                if move.endCol == 7:
                    tmpCastle.bKs = False
                elif move.endCol == 0:
                    tmpCastle.bQs = False

        self.castlesLog.append(CastleRights(tmpCastle.wQs, tmpCastle.wKs, tmpCastle.bQs,
                                            tmpCastle.bKs))  # Append same object with new values => different object
        self.currentCastles = tmpCastle  # Set the new rights

        # Function to determine which castle moves are allowed for the king
    def getCastle(self, row, col, moveList):
        # 1st condition : no check
        if self.isAttacked(row, col):
            return  # Unable to castle
        if (self.whiteTurn and self.currentCastles.wKs) or (not self.whiteTurn and self.currentCastles.bKs):
            self.getKingSide(row, col, moveList)
        if (self.whiteTurn and self.currentCastles.wQs) or (not self.whiteTurn and self.currentCastles.bQs):
            self.getQueenSide(row, col, moveList)

    # Helper function to determine if squares on each side are under attack
    def getKingSide(self, row, col, moveList):
        if 0 <= col + 2 <= 7:

            # 2nd condition : all between squares are free
            if self.board[row][col+1] == "  " and self.board[row][col+2] == "  ":  # Check if squares between both are free

                # 3rd condition : No between squares attacked
                if not self.isAttacked(row, col+1) and not self.isAttacked(row, col+2):
                    moveList.append(Move((row, col), (row, col+2), self.board, isCastle=True))  # Append the wKs castle move

    def getQueenSide(self, row, col, moveList):
        if 0 <= col - 3 <= 7:

            # 2nd condition : all between squares are free
            if self.board[row][col - 1] == "  " \
                    and self.board[row][col - 2] == "  " \
                    and self.board[row][col - 3] == "  ":  # Check if squares between both are free

                # 3rd condition : No between squares attacked
                if not self.isAttacked(row, col - 1) and not self.isAttacked(row, col - 2):
                    moveList.append(Move((row, col), (row, col - 2), self.board, isCastle=True))  # Append the wKs castle move

# --------------------------------------------------
# Class to create move object
class Move():

    def __init__(self, startSq, endSq, board, isEp=False, isCastle=False):
        self.startRow, self.startCol = startSq  # startSq = (row,col)
        self.endRow, self.endCol = endSq  # endSq = (row,col)
        self.pieceMoved = board[self.startRow][self.startCol]  # Piece that initialize the move
        self.pieceCaptured = board[self.endRow][self.endCol]  # Piece that end the move
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol  # Get a moveID with startSq and endSq
        # print(self.moveID)

        # Flags for pawn promotion
        self.isProm = self.isPromoting()    # Flag to know if the current move is a pawn prom
        self.promChoice = "Q"

        # Flags for en-passant moves
        self.isEp = isEp  # Flag to know if the current move is an ep move
        self.epPieceCaptured = "bP" if self.pieceMoved == "wP" else "wP"  # What piece is captured on en passant

        # Flags for castle moves
        self.isCastle = isCastle  # Flag to know if the current move is castling move

    # Overriding the equals method to be used with object
    def __eq__(self, other):
        if isinstance(other, Move):  # Return true if other object is from the class Move
            return self.moveID == other.moveID
        return False

    # def getChessNot(self, gs):
    #     moveCode = self.getRankFile(self.endRow, self.endCol)

    #     # Pawn promotion chess not
    #     if self.isProm:
    #         if self.pieceCaptured == "  ":  # If empty space => push
    #             chessNot = moveCode + "=" + self.promChoice  # i.e : "e8=Q"
    #         else:  # If not empty square => capture
    #             #print("capture")
    #             chessNot = self.getRankFile(self.startRow, self.startCol)[0] + "x" + moveCode + "=" + self.promChoice  # i.e : "exd8=Q"
        
    #     # Castling chess not
    #     if self.isCastle:
    #         if self.endCol == 6:  # King side
    #             chessNot = "0-0"
    #         else:  # Queen side
    #             chessNot = "0-0-0"
        
    #     # En-passant chess not
    #     if self.isEp:
    #         chessNot = self.getRankFile(self.startRow, self.startCol)[0] + "x" + moveCode + " e.p."  # i.e : "exd6 e.p."
        
    #     # Normal move chess not
    #     if self.pieceCaptured != "  ":  # If not empty space => capture
    #         if self.pieceMoved[1] == "P":
    #             chessNot = self.getRankFile(self.startRow, self.startCol)[0] + "x" + moveCode  # i.e : "exd5"
    #         else:
    #             chessNot = self.pieceMoved[1] + "x" + moveCode  # i.e : "Nxc3"
        
    #     else:  # If empty space => push
    #         if self.pieceMoved[1] == "P":
    #             chessNot = moveCode
    #         else:
    #             chessNot = self.pieceMoved[1] + moveCode

    #     if gs.checkmate:
    #         chessNot += "#"
    #         chessNot += "1-0" if not gs.whiteTurn else "0-1"  # If black turn => white won
    #     elif gs.stalemate:
    #         chessNot += "1/2-1/2"
    #     elif gs.inCheck:
    #         chessNot += "+"

    #     return chessNot

    # Function to get a complete chess notation
    def getChessNot(self, gs, isLastMove=False):
        moveCode = self.getRankFile(self.endRow, self.endCol)
        chessNot = ""

        # Pawn promotion chess notation
        if self.isProm:
            if self.pieceCaptured == "  ":  # If empty space => push
                chessNot = moveCode
            else:  # If not empty square => capture
                chessNot = self.getRankFile(self.startRow, self.startCol)[0] + "x" + moveCode
            chessNot += "=" + self.promChoice  # Append promotion choice (i.e.: "=Q")

        # Castling chess notation (e.g., "0-0" or "0-0-0")
        elif self.isCastle:
            chessNot = "0-0" if self.endCol == 6 else "0-0-0"

        # En-passant chess notation (e.g., "exd6 e.p.")
        elif self.isEp:
            chessNot = self.getRankFile(self.startRow, self.startCol)[0] + "x" + moveCode + " e.p."

        # Normal move chess notation
        else:
            if self.pieceCaptured != "  ":  # If not empty space => capture
                if self.pieceMoved[1] == "P":  # If pawn => file + "x" + square
                    chessNot = self.getRankFile(self.startRow, self.startCol)[0] + "x" + moveCode  
                else:  # If piece => piece symbol + "x" + square
                    chessNot = self.pieceMoved[1] + "x" + moveCode  
            else:  # If empty space => push
                if self.pieceMoved[1] == "P":  # If pawn => just square
                    chessNot = moveCode
                else:  # If piece => piece symbol + square
                    chessNot = self.pieceMoved[1] + moveCode

        # Append check, checkmate, or stalemate notation
        if isLastMove:
            if gs.checkmate:
                chessNot += "#"
                chessNot += "1-0" if not gs.whiteTurn else "0-1"  # If black turn => white won
            elif gs.stalemate:
                chessNot += "1/2-1/2"
            elif gs.inCheck:
                chessNot += "+"

        return chessNot

    # Function to get the right square id in chess notation
    def getRankFile(self, row, col):
        # Mapping the board by using a dict that convert indexes into chess notation
        # key : value ==> chess not : index
        ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        # .items() ==> [(k,v),(k,v),...]
        rowsToRanks = {v: k for k, v in ranksToRows.items()}
        # key : value ==> chess not : index
        filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        # .items() ==> [(k,v),(k,v),...]
        colsToFiles = {v: k for k, v in filesToCols.items()}

        # Get the chess notation of the square (i.e : "e4")
        return colsToFiles[col] + rowsToRanks[row]

    # Function to determine if the current move is a pawn promotion
    def isPromoting(self):
        return (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7)

# --------------------------------------------------
# Class to create right of castling object
class CastleRights():

    def __init__(self, wQs, wKs, bQs, bKs):
        self.wQs = wQs
        self.wKs = wKs
        self.bQs = bQs
        self.bKs = bKs

