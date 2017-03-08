from piece_types import *
from moves_of_pieces import *
from move import *
from evaluation import *

class Search:
    def __init__(self, position, default_depth=2):
        self.position = position
        self.default_depth = default_depth
        
    def evaluate(self):
        evaluation = 0
        for i in range(2, 10):
            for j in range(2, 10):
                tmp = self.position.board[i][j]
                evaluation += PST[tmp][i - 2][j - 2]
        return evaluation
    
    def quiescence(self, alpha, beta):
        evaluation = self.evaluate() * self.position.turn_to_move       
        if evaluation >= beta:
            return evaluation
        if evaluation > alpha:
            alpha = evaluation
        possible_moves = self.position.generate_captures()
        if len(possible_moves) == 0:
            return evaluation         
        for move in possible_moves:
            self.position.make_move(move)
            score = -self.quiescence(-beta, -alpha)
            self.position.unmake_move(move)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha
    
    def alphabeta(self, alpha, beta, depth):
        possible_moves = self.position.generate_moves()
        if len(possible_moves) == 0:
            if self.position.in_check(self.turn_to_move):
                return LOSING
            return DRAW
        if depth == 0:
            return self.quiescence(alpha, beta)
        possible_moves.sort(key=captures_in_begin)
        for move in possible_moves:
            self.position.make_move(move)
            score = -self.alphabeta(-beta, -alpha, depth-1)
            self.position.unmake_move(move)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha
    
    def get_best_move(self):
        alpha, beta = -1000000, 1000000
        bestmove = None
        possible_moves = self.position.generate_moves()
        possible_moves.sort(key=captures_in_begin)
        for move in possible_moves:
            self.position.make_move(move)
            score = -self.alphabeta(-beta, -alpha, self.default_depth-1)
            self.position.unmake_move(move)
            if score > alpha:
                bestmove = move
                alpha = score
        return bestmove
