# Engine class -- Responsible of storing datas & moves log + determining valid moves

class GameState():
    def __init__(self):
        # Initial board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # assign a letter to its move function
        self.RightMovFunc = {"P": self.GetPawnMoves, "K": self.GetKingMoves, "Q": self.GetQueenMoves,
                             "B": self.GetBishopMoves, "N": self.GetKnightMoves, "R": self.GetRookMoves}
        # Bool variable to determine which side has to play
        self.whiteTurn = True
        # List of every moves log
        self.moveLogList = []

    # Moving the piece and let leaved case in blank
    # A régler : Promotion / En-passant / Roque
    def MakeMove(self, move):
        self.board[move.startRow][move.startCol] = "  "
        self.board[move.endRow][move.endCol] = move.pieceMov
        print(move)
        self.moveLogList.append(move)# Log the move to undo or display it
        self.whiteTurn = not self.whiteTurn

    # Undoing the move just hapended
    def UndoMove(self):
        if len(self.moveLogList) != 0:  # make sure there is a move to undo
            move = self.moveLogList.pop()  # Unlog the move
            self.board[move.startRow][move.startCol] = move.pieceMov
            self.board[move.endRow][move.endCol] = move.pieceCapt
            self.whiteTurn = not self.whiteTurn

    # Checking at each moves if king is check
    def GetValidMoves(self):
        return self.GetPossibleMoves()  # Don't check if there is checks

    def GetPossibleMoves(self):
        moves = []  # list of available moves
        for r in range(len(self.board)):# number of rows
            for c in range(len(self.board[r])):  # number of columns in given rows
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteTurn) or (turn == "b" and not self.whiteTurn):
                    piece = self.board[r][c][1]
                    moves.append(self.RightMovFunc[piece](r, c, self.board))  # call the right function
        return moves

    # Identify valid (non special) pawn moves
    def GetPawnMoves(self, r, c, moves):
        if self.whiteTurn:  # white
            if self.board[r - 1][c] == "  ":  # normal (1 square ahead) white pawn move
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "  ":  # start (2 square ahead) white pawn move
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # check if the pawn is not in the left border to be able to capture
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # check if the pawn is not in the right border to be able to capture
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # black
            if self.board[r + 1][c] == "  ":  # normal (1 square ahead) black pawn move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "  ":  # start (2 square ahead) black pawn move
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c + 1 >= 0:  # check if the pawn is not in the left border to be able to capture
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # check if the pawn is not in the right border to be able to capture
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
        return moves

    # Identify valid (non special) king moves
    def GetKingMoves(self, r, c, moves):
        dir = ((1, -1), (1, 0), (1, 1), (-1, -1), (-1, 0), (-1, 1), (0, -1),(0, 1))  # directions king able to move
            # (down-left,down,down-right,up-left,up,up-right,left,right)
        ally = "w" if self.whiteTurn else "b"
        for i in range(8):
            endRow = r + dir[i][0]
            endCol = c + dir[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # check if on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:  # check if target case is an ally
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # Identify valid queen moves
    def GetQueenMoves(self, r, c, moves):
        self.GetRookMoves(r, c, self.board)
        self.GetBishopMoves(r, c, self.board)

    # Identify valid bishop moves
    def GetBishopMoves(self, r, c, moves):
        dir = ((-1, -1), (1, -1), (1, 1), (-1, 1))  # directions bishop able to move
        #   (left-up,left-down,right-up,right-down)
        enemy = "b" if self.whiteTurn else "w"
        for d in dir:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # check if on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "  ":  # check if target case is free
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:  # check if target case is an enemy
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # ally piece
                        break
                else:  # out of board
                    break

    # Identify valid knight moves
    def GetKnightMoves(self, r, c, moves):
        knightMove = (
        (-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2))  # directions knight able to move
        #(up-left,up-right,down-left,down-right,left-up,left-down,right-up,right-down)
        ally = "w" if self.whiteTurn else "b"
        for m in knightMove:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # check if on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:  # check if target case is an ally
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # Identify valid rook moves
    def GetRookMoves(self, r, c, moves):
        dir = ((-1, 0), (1, 0), (0, -1), (0, 1))  # directions rook able to move (up,down,left,right)
        enemy = "b" if self.whiteTurn else "w"
        for d in dir:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # check if on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "  ":  # check if target case is free
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:  # check if target case is an enemy
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # ally piece
                        break
                else:  # out of board
                    break


class Move():
    # Identify square notations with the number of their row and col
    rowToRanks = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1,
                  "8": 0}  # Assign a row number chess notation to a row number computer notation
    ranksToRow = {v: k for k, v in rowToRanks.items()}
    colToFiles = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6,
                  "h": 7}  # Assign a col number chess notation to a col number computer notation
    filesToCol = {v: k for k, v in colToFiles.items()}

    # Requirement to any moves (piece moved/piece captured/start move/end move)
    def __init__(self, sqStart, sqEnd, board):
        self.startRow = sqStart[0]
        self.startCol = sqStart[1]
        self.endRow = sqEnd[0]
        self.endCol = sqEnd[1]
        self.pieceMov = board[self.startRow][self.startCol]
        self.pieceCapt = board[self.endRow][self.endCol]
        self.MoveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol  # MoveID = xxxx (x in [0;7])
        """print(self.MoveID)"""

    # Comparing this object to others
    def __eq__(self, other):
        if isinstance(other, Move):  # Return true if "other" object is a class type
            # https://www.w3schools.com/python/trypython.asp?filename=demo_ref_isinstance3
            return self.MoveID == other.MoveID
        return False

    # Making a simplified chess notation of the squares
    def GetChessNot(self):
        # /!\ possibilité d'ajouter le type de piece pour avoir une vraie notation (nom des piece et x quand capture)
        """p = self.board[self.startRow][self.startCol][1]
        if p != "P":
            return p + self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        else:
            return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    # Assign a rank and a file to a row and col number
    def getRankFile(self, r, c):
        return self.filesToCol[c] + self.ranksToRow[r]
