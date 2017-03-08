from position import Position
from search import Search
from move import Move
import piece_types as ptypes
from collections import defaultdict 

class Game:    
    def __init__(self, our_color=ptypes.WHITE):
        self.position = Position()
        self.our_color = our_color
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
            return "����� ��-�� ������������ ���������� �����"
        if self.is_draw_by_fifty_moves():
            return "����� �� ������� ���������� �����"
        if self.is_stalemate():
            if self.position.turn_to_move == self.our_color:
                return "��� ��������� ���. �����"
            return "�� ��������� ���. �����"
        if self.is_mate():
            if self.position.turn_to_move == self.our_color:
                return "��� ��������� ��� :("
            return "�� ��������� ���. ����������!"
        return None    
    
    def string_to_move(self, string):
        string = string.lower().replace(' ', '')
        str_to_piece = {
            'q': ptypes.QUEEN,
            'r': ptypes.ROOK,
            'b': ptypes.BISHOP,
            'n': ptypes.KNIGHT
        }
        vertical   = dict(zip("abcdefgh", range(2, 10)))
        horizontal = dict(zip("12345678", range(2, 10)))
        start = to = turn = 0
        if len(string) == 5:
            if string[4] not in str_to_piece:
                return None
            turn = str_to_piece[string[4]]
        elif len(string) != 4:
            return None
        if not(string[0] in vertical   and string[2] in vertical and
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


def run():
    game = Game(ptypes.WHITE)
    print(game.position)
    while True:
        verdict = game.get_end_verdict()
        if verdict:
            print(verdict)
            return
        move = None
        if game.position.turn_to_move == game.our_color:
            while not move:
                move = game.string_to_move(input())
                if not move:
                    print("������������ ������ ����� ��� ��� ����������")
        else:
            move = game.get_move_of_bot()
        game.make_move(move)
        print(game.position)
                                           
    
    
if __name__ == "__main__":
    run()
    