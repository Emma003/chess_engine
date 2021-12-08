# Storing all info about the current state of a chess game
# Determines valid moves
# Keeps move log

import numpy as np

# Using a 2D list (consider using a numpy 2d array)
class GameState():

    # Constructor
    def __init__(self):

        # Representing the board as a 2d numpy array
        # b/w: black/white; second letter is the piece type
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["**", "**", "**", "**", "**", "**", "**", "**"],
            ["**", "**", "**", "wQ", "**", "**", "**", "**"],
            ["**", "**", "**", "**", "**", "**", "**", "**"],
            ["**", "**", "**", "**", "**", "**", "**", "**"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        self.white_to_move = True
        self.move_log = []

    # takes a move as parameter and executes it (doesn't work for castling, en-passant and pawn-promotion
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "**"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # records move so it can be undone
        self.white_to_move = not self.white_to_move # swaps players

    #undoes last move
    def undo_move(self):
        if len(self.move_log) != 0: #makes sure the move log isn't empty
            move = self.move_log.pop() #.pop() returns the last item in the list AND removes it
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move #switch turns back

    #all moves considering checks
    def get_valid_moves(self):
        return self.get_all_possible_moves()

    #all moves without considering checks
    def get_all_possible_moves(self):
        #all the moves will be added to this list
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                #accessing the first character of a given square on the board (b, w or *)
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    #accessing piece type
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.get_pawn_moves(r, c, moves)
                    elif piece == 'R':
                        self.get_rook_moves(r, c, moves)
                    elif piece == 'N':
                        self.get_knight_moves(r, c, moves)
                    elif piece == 'B':
                        self.get_bishop_moves(r, c, moves)
                    elif piece == 'Q':
                        self.get_queen_moves(r, c, moves)
                        ''' 
                    elif piece == 'Q':
                    elif piece == 'K':
                    elif piece == 'B':
                    elif piece == 'N':
                        '''
        return moves

    #get all possible moves for the pawn located at r and c and add them to the list
    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move: #white to move
            #forward movements
            if self.board[r-1][c] == "**": #1 square pawn advance
                moves.append(Move((r,c),(r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "**": #2 square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            #diagonal movements
            if 0 < c < 7: #if the piece isn't one of the edge pieces
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture (black)
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
            if c == 0: #the leftmost piece
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
            if c >= 7: #the rightmost piece
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
        else: #black to move
            # forward movements
            if self.board[r + 1][c] == "**":  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "**":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # diagonal movements
            if 0 < c < 7:  # if the piece isn't one of the edge pieces
                if self.board[r + 1][c - 1][0] == 'w':  # enemy piece to capture (white)
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if c == 0:  # the leftmost piece
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if c >= 7:  # the rightmost piece
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

    # get all possible moves for the rook located at r and c and add them to the list
    #IMPROVE DESIGN WHEN YOU CAN (MAYBE CREATE A SINGLE FUNCTION THAT GETS PASSED A LIST OF DIRECTIONS DEPENDING ON THE PIECE)
    def get_rook_moves(self, r, c, moves):
        if self.white_to_move:
            friend = 'w'
            enemy = 'b'
        else:
            friend = 'b'
            enemy = 'w'

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) # top, bottom, left, right
        for d in directions:
            for i in range(1,8):
                final_row = r + (i * d[0])
                final_column = c + (i * d[1])
                if 0 <= final_row <= 7 and 0 <= final_column <= 7:
                    if self.board[final_row][final_column] == "**":  # empty square
                        moves.append(Move((r, c), (final_row, final_column), self.board))
                        continue
                    elif self.board[final_row][final_column][0] == enemy:  # square occupied by enemy piece
                        moves.append(Move((r, c), (final_row, final_column), self.board))
                        break
                    elif self.board[final_row][final_column][0] == friend:  # square occupied by friendly piece
                        break


    # get all possible moves for the knight located at r and c and add them to the list
    def get_knight_moves(self, r, c, moves):
        if self.white_to_move:
            friend = 'w'
            enemy = 'b'
        else:
            friend = 'b'
            enemy = 'w'

        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2))  # top, bottom, left, right
        for d in directions:
                final_row = r + d[0]
                final_column = c + d[1]
                if 0 <= final_row <= 7 and 0 <= final_column <= 7:
                    if self.board[final_row][final_column] == "**" or self.board[final_row][final_column] == enemy:  # empty or enemy occupied square
                        moves.append(Move((r, c), (final_row, final_column), self.board))
                    elif self.board[final_row][final_column][0] == friend:  # square occupied by friendly piece
                        continue

    # get all possible moves for the bishop located at r and c and add them to the list
    def get_bishop_moves(self, r, c, moves):
        if self.white_to_move:
            friend = 'w'
            enemy = 'b'
        else:
            friend = 'b'
            enemy = 'w'

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # top-left, top-right, bottom-left, bottom-right
        for d in directions:
            for i in range(1,8):
                final_row = r + (i * d[0])
                final_column = c + (i * d[1])
                if 0 <= final_row <= 7 and 0 <= final_column <= 7:
                    if self.board[final_row][final_column] == "**":  # empty square
                        moves.append(Move((r, c), (final_row, final_column), self.board))
                        continue
                    elif self.board[final_row][final_column][0] == enemy:  # square occupied by enemy piece
                        moves.append(Move((r, c), (final_row, final_column), self.board))
                        break
                    elif self.board[final_row][final_column][0] == friend:  # square occupied by friendly piece
                        break

    def get_king_moves(self, r, c, moves):
        if self.white_to_move:
            friend = 'w'
            enemy = 'b'
        else:
            friend = 'b'
            enemy = 'w'

        directions = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1))  # top, bottom, left, right
        for d in directions:
                final_row = r + d[0]
                final_column = c + d[1]
                if 0 <= final_row <= 7 and 0 <= final_column <= 7:
                    if self.board[final_row][final_column] == "**" or self.board[final_row][final_column] == enemy:  # empty or enemy occupied square
                        moves.append(Move((r, c), (final_row, final_column), self.board))
                    elif self.board[final_row][final_column][0] == friend:  # square occupied by friendly piece
                        continue

    # get all possible moves for the queen located at r and c and add them to the list
    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r,c,moves)
        self.get_bishop_moves(r, c, moves)

class Move():

    # translating the 2d array to ranks and files (chess notation) using dictionaries
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v:k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    # passing the board as a parameter so the info about piece moves can be stored (easier to undo moves)
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        #giving a unique move id parameter that is going to be used for comparison (similar to a hash code)
        #the move id will be a unique value from 0-7777
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        print(self.move_id)

    #overrides equals method for comparing moves
    def __eq__(self, other):
        if isinstance(other, Move):
           return self.move_id == other.move_id
        return False


    # returns rank-file notation for the move (start-end pair)
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    # returns rank-file notation for a single square on the board
    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]