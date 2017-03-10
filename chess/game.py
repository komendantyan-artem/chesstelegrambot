# -*- coding: utf-8 -*-

from .position import Position
from .search import Search
from .move import Move
from . import piece_types as ptypes
from collections import defaultdict


class Game:
    def __init__(self, color):
        assert(color in ["white", "black"])
        self.position = Position()
        self.our_color = ptypes.WHITE if color == "white" else ptypes.BLACK
        self.is_reversed_image = (self.our_color == ptypes.BLACK)
        self.positions_count = defaultdict(int)
        self.number_of_insignificant_plies = 0
        self.positions_count[repr(self.position)] += 1

    def make_move(self, move):
        piece = self.position.board[move.start[0]][move.start[1]]
        if ptypes.type_of(piece) == ptypes.PAWN:
            self.number_of_insignificant_plies = 0
        elif move.broken:
            self.number_of_insignificant_plies = 0
        else:
            self.number_of_insignificant_plies += 1
        self.position.make_move(move)
        self.positions_count[repr(self.position)] += 1

    def is_draw_by_repetion(self):
        for position in self.positions_count:
            if self.positions_count[position] >= 3:
                return True
        return False

    def is_draw_by_fifty_moves(self):
        return self.number_of_insignificant_plies >= 2 * 50

    def is_stalemate(self):
        if self.position.generate_moves():
            return False
        return not self.position.in_check(self.position.turn_to_move)

    def is_mate(self):
        if self.position.generate_moves():
            return False
        return self.position.in_check(self.position.turn_to_move)

    def get_end_verdict(self):
        if self.is_draw_by_repetion():
            return "Ничья из-за трехкратного повторения ходов"
        if self.is_draw_by_fifty_moves():
            return "Ничья по правилу пятидесяти ходов"
        if self.is_stalemate():
            if self.position.turn_to_move == self.our_color:
                return "Вам поставили пат. Ничья"
            return "Вы поставили пат. Ничья"
        if self.is_mate():
            if self.position.turn_to_move == self.our_color:
                return "Вам поставили мат :("
            return "Вы поставили мат. Поздравляю!"
        return None

    def string_to_move(self, string):
        string = string.lower().replace(' ', '')
        str_to_piece = {
            'q': ptypes.QUEEN,
            'r': ptypes.ROOK,
            'b': ptypes.BISHOP,
            'n': ptypes.KNIGHT
        }
        vertical = dict(zip("abcdefgh", range(2, 10)))
        horizontal = dict(zip("12345678", range(2, 10)))
        start = to = turn = 0
        if len(string) == 5:
            if string[4] not in str_to_piece:
                return None
            turn = str_to_piece[string[4]]
        elif len(string) != 4:
            return None
        if not(string[0] in vertical and string[2] in vertical and
               string[1] in horizontal and string[3] in horizontal):
            return None
        start = (horizontal[string[1]], vertical[string[0]])
        to = (horizontal[string[3]], vertical[string[2]])
        for move in self.position.generate_moves():
            if (move.start, move.to, move.turn) == (start, to, turn):
                return move
        return None

    def get_move_of_bot(self):
        return Search(self.position).get_best_move()
    
    def start_game(self):
        if self.position.turn_to_move == self.our_color:
            return [self.position.get_fen(reverse=self.is_reversed_image)]
        else:
            self.make_move(self.get_move_of_bot())
            return [self.position.get_fen(reverse=self.is_reversed_image)]
        
    def step(self, string):
        move = self.string_to_move(string)
        if not move:
            return "Неправильный формат ввода или ход невозможен"
        result = []
        self.make_move(move)
        result.append(self.position.get_fen(reverse=self.is_reversed_image))
        if self.get_end_verdict():
            return result
        self.make_move(self.get_move_of_bot())
        result.append(self.position.get_fen(reverse=self.is_reversed_image))
        return result