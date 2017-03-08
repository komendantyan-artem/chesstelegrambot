from piece_types import *
from moves_of_pieces import *
from evaluation import *
from move import *
import move_generation

class Position:
    def __init__(self):
        self.board = [[0 for i in range(12)] for j in range(12)]
        for i in range(12):
            for j in range(2):
                self.board[i][j] = BORDER
                self.board[i][11 - j] = BORDER
                self.board[j][i] = BORDER
                self.board[11 - j][i] = BORDER
        self.turn_to_move = 0
        self.castling = [0] * 4
        self.en_passant = 0
        self.setup()

    def __str__(self):
        piece_to_str = dict(zip(list(range(1, 7)) + list(range(-1,-7,-1)) + [0],
                             "KQRBNPkqrbnp."))
        string = ""
        for i in reversed(self.board[2:10]):
            string += '\n'
            for j in i[2: 10]:
                string += piece_to_str[j]
        return string
    
    def __repr__(self):
        return (repr(self.board) + repr(self.turn_to_move) +
                repr(self.castling) + repr(self.en_passant))

    def setup(self, fen=None):
        if fen == None:
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        tmp = fen.split()
        arrangement_of_pieces = tmp[0]
        turn_to_move           = tmp[1]
        possible_castling      = tmp[2]
        en_passant             = tmp[3]
        number_of_insignificant_plies = int(tmp[4])
        number_of_moves               = int(tmp[5])
        horizontal, vertical = 9, 2
        str_to_piece = dict(zip("KQRBNPkqrbnp",
                             list(range(1, 7)) + list(range(-1,-7,-1))))
        for i in arrangement_of_pieces:
            if i == '/':
                horizontal -= 1
                vertical = 2
            elif i in str_to_piece:
                self.board[horizontal][vertical] = str_to_piece[i]
                vertical += 1
            else:
                number = int(i)
                for j in range(number):
                    self.board[horizontal][vertical+j] = 0
                vertical += number
        self.turn_to_move = WHITE if turn_to_move == 'w' else BLACK
        self.castling[0] = int('K' in possible_castling)
        self.castling[1] = int('Q' in possible_castling)
        self.castling[2] = int('k' in possible_castling)
        self.castling[3] = int('q' in possible_castling)
        if en_passant != '-':
            self.en_passant = 2 + "abcdefgh".index(en_passant[0])
        else:
            self.en_passant = 0
    
    def make_move(self, move):
        move.copies_of_flags = (self.castling[:], self.en_passant)
        h1, v1 = move.start
        h2, v2 = move.to
        piece = self.board[h1][v1]
        self.board[h2][v2] = piece
        self.board[h1][v1] = 0
        if move.turn != 0:
            self.board[h2][v2] = move.turn
        if move.en_passant:
            self.board[h1][v2] = 0
        if type_of(piece) == PAWN and abs(h1 - h2) == 2:
            self.en_passant = v1
        else:
            self.en_passant = 0
        if type_of(piece) == KING:
            add_to_index = 0 if self.turn_to_move == WHITE else 2
            self.castling[add_to_index] = 0
            self.castling[1 + add_to_index] = 0
            if v1 - v2 == 2:
                self.board[h1][5] = self.board[h1][2]
                self.board[h1][2] = 0
            elif v2 - v1 == 2:
                self.board[h1][7] = self.board[h1][9]
                self.board[h1][9] = 0
        for color_of_rooks in (1, -1):
            add_to_index = 0 if color_of_rooks == 1 else 2
            horizontal = 2 if color_of_rooks == 1 else 9
            if self.board[horizontal][9] != color_of_rooks * ROOK:
                self.castling[add_to_index] = 0
            if self.board[horizontal][2] != color_of_rooks * ROOK:
                self.castling[1 + add_to_index] = 0
        self.turn_to_move = -self.turn_to_move

    def unmake_move(self, move):
        self.castling, self.en_passant = move.copies_of_flags
        self.turn_to_move = -self.turn_to_move
        h1, v1 = move.start
        h2, v2 = move.to
        self.board[h1][v1] = self.board[h2][v2]
        self.board[h2][v2] = move.broken
        piece = self.board[h1][v1]
        if move.turn != 0:
            self.board[h1][v1] = PAWN * self.turn_to_move
        elif move.en_passant:
            self.board[h2][v2] = 0
            self.board[h1][v2] = move.broken
        elif type_of(piece) == KING and abs(v1 - v2) == 2:
            if v2 < v1:
                self.board[h1][2] = self.board[h1][5]
                self.board[h1][5] = 0
            else:
                self.board[h1][9] = self.board[h1][7]
                self.board[h1][7] = 0

    def in_check(self, color_of_king):
        place_of_king = None
        for i in range(2, 10):
            for j in range(2, 10):
                tmp = self.board[i][j]
                if self.board[i][j] == KING * color_of_king:
                    place_of_king = (i, j)
                    break
            if place_of_king != None:
                break
        x, y = place_of_king
        direction_of_pawns = color_of_king
        for k in (1, -1):
            tmp = self.board[x + direction_of_pawns][y + k]
            if tmp == -color_of_king * PAWN:
                return True
        for k, l in moves_of_knight:
            tmp = self.board[x + k][y + l]
            if tmp == -color_of_king * KNIGHT:
                return True
        for k, l in moves_of_king:
            tmp = self.board[x + k][y + l]
            if tmp == -color_of_king * KING:
                return True
        for k, l in directions_of_rook:
            for n in range(1, 10):
                tmp = self.board[x + k*n][y + l*n]
                if (color_of(tmp) == -color_of_king and
                type_of(tmp) in (QUEEN, ROOK)):
                    return True
                if tmp != 0:
                    break
        for k, l in directions_of_bishop:
            for n in range(1, 10):
                tmp = self.board[x + k*n][y + l*n]
                if (color_of(tmp) == -color_of_king and
                type_of(tmp) in (QUEEN, BISHOP)):
                    return True
                if tmp != 0:
                    break
        return False

    generate_moves = move_generation.generate_moves
    generate_captures = move_generation.generate_captures
    
    def evaluate(self):
        evaluation = 0
        for i in range(2, 10):
            for j in range(2, 10):
                tmp = self.board[i][j]
                evaluation += PST[tmp][i - 2][j - 2]
        return evaluation
    
    def quiescence(self, alpha, beta):
        evaluation = self.evaluate() * self.turn_to_move       
        if evaluation >= beta:
            return evaluation
        if evaluation > alpha:
            alpha = evaluation
        possible_moves = self.generate_captures()
        if len(possible_moves) == 0:
            return evaluation         
        for move in possible_moves:
            self.make_move(move)
            score = -self.quiescence(-beta, -alpha)
            self.unmake_move(move)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha
    
    def alphabeta(self, alpha, beta, depth):
        possible_moves = self.generate_moves()
        if len(possible_moves) == 0:
            if self.in_check(self.turn_to_move):
                return LOSING
            return DRAW
        if depth == 0:
            return self.quiescence(alpha, beta)
        possible_moves.sort(key=captures_in_begin)
        for move in possible_moves:
            self.make_move(move)
            score = -self.alphabeta(-beta, -alpha, depth-1)
            self.unmake_move(move)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha
    
    def search(self, depth=2):
        alpha, beta = -1000000, 1000000
        bestmove = None
        possible_moves = self.generate_moves()
        possible_moves.sort(key=captures_in_begin)
        for move in possible_moves:
            self.make_move(move)
            score = -self.alphabeta(-beta, -alpha, depth-1)
            self.unmake_move(move)
            if score > alpha:
                bestmove = move
                alpha = score
        return bestmove
                    

def parse_move(string):
    turn = {'q': QUEEN, 'r': ROOK, 'b': BISHOP, 'n': KNIGHT}
    vertical   = dict(zip("abcdefgh", range(2, 10)))
    horizontal = dict(zip("12345678", range(2, 10)))
    result = [0 for i in range(3)]
    if len(string) == 5:
        if string[4] not in turn:
            return None
        result[2]  = turn[string[4]]
    elif len(string) != 4:
        return None
    if not(string[0] in vertical   and string[2] in vertical and
           string[1] in horizontal and string[3] in horizontal):
        return None
    result[0] = (horizontal[string[1]], vertical[string[0]])
    result[1] = (horizontal[string[3]], vertical[string[2]])
    return result
    

if __name__ == "__main__":
    default_depth = 2
    p = Position()
    while True:
        print(p)
        possible_moves = p.generate_moves()
        while True:
            move = parse_move(input())
            if move == None:
                continue
            flag = 0
            for i in possible_moves:
                if move[0] == i.start and move[1] == i.to:
                    i.turn = move[2]
                    p.make_move(i)
                    flag = 1
                    break
            if flag:
                break
        
        print(p)
        bestmove = p.search(depth=default_depth)
        if bestmove == None:
            break
        p.make_move(bestmove)