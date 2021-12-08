
'''
# get all possible moves for the rook located at r and c and add them to the list
# IMPROVE DESIGN WHEN YOU CAN (MAYBE CREATE A SINGLE FUNCTION THAT GETS PASSED A LIST OF DIRECTIONS DEPENDING ON THE PIECE)
def get_rook_moves(self, r, c, moves):
    if self.white_to_move:  # white to move
        # forward movements (white)
        fw = 1
        while r - fw >= 0:
            if self.board[r - fw][c] == "**":  # empty square
                moves.append(Move((r, c), (r - fw, c), self.board))
                fw += 1
                continue
            elif self.board[r - fw][c][0] == 'w':  # square occupied by same coloured piece
                break
            elif self.board[r - fw][c][0] == 'b':  # square occupied by enemy piece
                moves.append(Move((r, c), (r - fw, c), self.board))
                break

        # backward movements (white)
        bw = 1
        while r + bw <= 7:
            if self.board[r + bw][c] == "**":  # empty square
                moves.append(Move((r, c), (r + bw, c), self.board))
                bw += 1
                continue
            elif self.board[r + bw][c][0] == 'w':  # square occupied by same coloured piece
                break
            elif self.board[r + bw][c][0] == 'b':  # square occupied by enemy piece
                moves.append(Move((r, c), (r + bw, c), self.board))
                break

        # left movements (white)
        lw = 1
        while c - lw >= 0:
            if self.board[r][c - lw] == "**":  # empty square
                moves.append(Move((r, c), (r, c - lw), self.board))
                lw += 1
                continue
            elif self.board[r][c - lw][0] == 'w':  # square occupied by same coloured piece
                break
            elif self.board[r][c - lw][0] == 'b':  # square occupied by enemy piece
                moves.append(Move((r, c), (r, c - lw), self.board))
                break

        # right movements (white)
        rightw = 1
        while c + rightw <= 7:
            if self.board[r][c + rightw] == "**":  # empty square
                moves.append(Move((r, c), (r, c + rightw), self.board))
                rightw += 1
                continue
            elif self.board[r][c + rightw][0] == 'w':  # square occupied by same coloured piece
                break
            elif self.board[r][c + rightw][0] == 'b':  # square occupied by enemy piece
                moves.append(Move((r, c), (r, c + rightw), self.board))
                break


    else:  # black to move
        # forward movements (black)
        fb = 1
        while r + fb <= 7:
            if self.board[r + fb][c] == "**":  # empty square
                moves.append(Move((r, c), (r + fb, c), self.board))
                fb += 1
                continue
            elif self.board[r + fb][c][0] == 'b':  # square occupied by same coloured piece
                break
            elif self.board[r + fb][c][0] == 'w':  # square occupied by enemy piece
                moves.append(Move((r, c), (r + fb, c), self.board))
                break

        # backward movements (black)
        bb = 1
        while r - bb >= 0:
            if self.board[r - bb][c] == "**":  # empty square
                moves.append(Move((r, c), (r - bb, c), self.board))
                bb += 1
                continue
            elif self.board[r - bb][c][0] == 'b':  # square occupied by same coloured piece
                break
            elif self.board[r - bb][c][0] == 'w':  # square occupied by enemy piece
                moves.append(Move((r, c), (r - bb, c), self.board))
                break

        # left movements (black)
        lb = 1
        while c - lb >= 0:
            if self.board[r][c - lb] == "**":  # empty square
                moves.append(Move((r, c), (r, c - lb), self.board))
                lb += 1
                continue
            elif self.board[r][c - lb][0] == 'b':  # square occupied by same coloured piece
                break
            elif self.board[r][c - lb][0] == 'w':  # square occupied by enemy piece
                moves.append(Move((r, c), (r, c - lb), self.board))
                break

        # right movements (black)
        rightb = 1
        while c + rightb <= 7:
            if self.board[r][c + rightb] == "**":  # empty square
                moves.append(Move((r, c), (r, c + rightb), self.board))
                rightb += 1
                continue
            elif self.board[r][c + rightb][0] == 'b':  # square occupied by same coloured piece
                break
            elif self.board[r][c + rightb][0] == 'w':  # square occupied by enemy piece
                moves.append(Move((r, c), (r, c + rightb), self.board))
                break

'''
