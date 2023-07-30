"""
Data storing class
"""


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

        ]
        self.WhiteTurn = True
        self.moveLog = []

    def make_move(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.WhiteTurn = not self.WhiteTurn

    def undo_move(self):
        print("undo")
        if self.moveLog == 0:
            return
        move = self.moveLog.pop()
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.WhiteTurn = not self.WhiteTurn

    def get_valid_moves(self):
        # TODO
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.WhiteTurn) or (turn == 'b' and not self.WhiteTurn):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.WhiteTurn:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0 and self.board[r - 1][c - 1][0] == 'b':
                moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 < len(self.board[r]) and self.board[r - 1][c + 1][0] == 'b':
                moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0 and self.board[r + 1][c - 1][0] == 'w':
                moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 < len(self.board[r]) and self.board[r + 1][c + 1][0] == 'w':
                moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = 'b' if self.WhiteTurn else 'w'
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        if self.WhiteTurn:
            if r + 2 < len(self.board) and c + 1 < len(self.board[r]) and \
                    (self.board[r + 2][c + 1] == "--" or self.board[r + 2][c + 1][0] == 'b'):
                moves.append(Move((r, c), (r + 2, c + 1), self.board))
            if r + 2 < len(self.board) and c - 1 >= 0 and \
                    (self.board[r + 2][c - 1] == "--" or self.board[r + 2][c - 1][0] == 'b'):
                moves.append(Move((r, c), (r + 2, c - 1), self.board))
            if r - 2 >= 0 and c + 1 < len(self.board[r]) and \
                    (self.board[r - 2][c + 1] == "--" or self.board[r - 2][c + 1][0] == 'b'):
                moves.append(Move((r, c), (r - 2, c + 1), self.board))
            if r - 2 >= 0 and c - 1 >= 0 and \
                    (self.board[r - 2][c - 1] == "--" or self.board[r - 2][c - 1][0] == 'b'):
                moves.append(Move((r, c), (r - 2, c - 1), self.board))
            if r + 1 < len(self.board) and c + 2 < len(self.board[r]) and \
                    (self.board[r + 1][c + 2] == "--" or self.board[r + 1][c + 2][0] == 'b'):
                moves.append(Move((r, c), (r + 1, c + 2), self.board))
            if r + 1 < len(self.board) and c - 2 >= 0 and \
                    (self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == 'b'):
                moves.append(Move((r, c), (r + 1, c - 2), self.board))
            if r - 1 >= 0 and c + 2 < len(self.board[r]) and \
                    (self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == 'b'):
                moves.append(Move((r, c), (r - 1, c + 2), self.board))
            if r - 1 >= 0 and c - 2 >= 0 and \
                    (self.board[r - 1][c - 2] == "--" or self.board[r - 1][c - 2][0] == 'b'):
                moves.append(Move((r, c), (r - 1, c - 2), self.board))
        else:
            if r + 2 < len(self.board) and c + 1 < len(self.board[r]) and \
                    (self.board[r + 2][c + 1] == "--" or self.board[r + 2][c + 1][0] == 'w'):
                moves.append(Move((r, c), (r + 2, c + 1), self.board))
            if r + 2 < len(self.board) and c - 1 >= 0 and \
                    (self.board[r + 2][c - 1] == "--" or self.board[r + 2][c - 1][0] == 'w'):
                moves.append(Move((r, c), (r + 2, c - 1), self.board))
            if r - 2 >= 0 and c + 1 < len(self.board[r]) and \
                    (self.board[r - 2][c + 1] == "--" or self.board[r - 2][c + 1][0] == 'w'):
                moves.append(Move((r, c), (r - 2, c + 1), self.board))
            if r - 2 >= 0 and c - 1 >= 0 and \
                    (self.board[r - 2][c - 1] == "--" or self.board[r - 2][c - 1][0] == 'w'):
                moves.append(Move((r, c), (r - 2, c - 1), self.board))
            if r + 1 < len(self.board) and c + 2 < len(self.board[r]) and \
                    (self.board[r + 1][c + 2] == "--" or self.board[r + 1][c + 2][0] == 'w'):
                moves.append(Move((r, c), (r + 1, c + 2), self.board))
            if r + 1 < len(self.board) and c - 2 >= 0 and \
                    (self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == 'w'):
                moves.append(Move((r, c), (r + 1, c - 2), self.board))
            if r - 1 >= 0 and c + 2 < len(self.board[r]) and \
                    (self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == 'w'):
                moves.append(Move((r, c), (r - 1, c + 2), self.board))
            if r - 1 >= 0 and c - 2 >= 0 and \
                    (self.board[r - 1][c - 2] == "--" or self.board[r - 1][c - 2][0] == 'w'):
                moves.append(Move((r, c), (r - 1, c - 2), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))
        enemyColor = 'b' if self.WhiteTurn else 'w'
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, r, c, moves):
        if r - 1 >= 0:
            if self.board[r - 1][c] == "--" or (self.WhiteTurn and self.board[r - 1][c][0] == 'b') \
                    or (not self.WhiteTurn and self.board[r - 1][c][0] == 'w'):
                moves.append(Move((r, c), (r - 1, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1] == "--" or (self.WhiteTurn and self.board[r - 1][c - 1][0] == 'b') \
                        or (not self.WhiteTurn and self.board[r - 1][c - 1][0] == 'w'):
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 < len(self.board[r]):
                if self.board[r - 1][c + 1] == "--" or (self.WhiteTurn and self.board[r - 1][c + 1][0] == 'b') \
                        or (not self.WhiteTurn and self.board[r - 1][c + 1][0] == 'w'):
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        if r + 1 < len(self.board):
            if self.board[r + 1][c] == "--" or (self.WhiteTurn and self.board[r + 1][c][0] == 'b') \
                    or (not self.WhiteTurn and self.board[r + 1][c][0] == 'w'):
                moves.append(Move((r, c), (r + 1, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1] == "--" or (self.WhiteTurn and self.board[r + 1][c - 1][0] == 'b') \
                        or (not self.WhiteTurn and self.board[r + 1][c - 1][0] == 'w'):
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 < len(self.board[r]):
                if self.board[r + 1][c + 1] == "--" or (self.WhiteTurn and self.board[r + 1][c + 1][0] == 'b') \
                        or (not self.WhiteTurn and self.board[r + 1][c + 1][0] == 'w'):
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
        if c - 1 >= 0:
            if self.board[r][c - 1] == "--" or (self.WhiteTurn and self.board[r][c - 1][0] == 'b') \
                    or (not self.WhiteTurn and self.board[r][c - 1][0] == 'w'):
                moves.append(Move((r, c), (r, c - 1), self.board))
        if c + 1 < len(self.board[r]):
            if self.board[r][c + 1] == "--" or (self.WhiteTurn and self.board[r][c + 1][0] == 'b') \
                    or (not self.WhiteTurn and self.board[r][c + 1][0] == 'w'):
                moves.append(Move((r, c), (r, c + 1), self.board))


class Move:
    ranksToRow = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRow.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, start, end, board):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startCol) + " --> " + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
