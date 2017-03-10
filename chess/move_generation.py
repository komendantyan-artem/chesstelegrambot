from .piece_types import *
from .moves_of_pieces import *
from .move import Move


def castling_is_possible(self, horizontal_of_king, which_castling):
    add_to_index = 0 if self.turn_to_move == 1 else 2
    if not self.castling[which_castling + add_to_index]:
        return False
    if self.in_check(self.turn_to_move):
        return False
    x = horizontal_of_king
    if which_castling == 0:
        for i in range(7, 9):
            if self.board[x][i] != 0:
                return False
        move = Move((x, 6), (x, 7))
    else:
        for i in range(3, 6):
            if self.board[x][i] != 0:
                return False
        move = Move((x, 6), (x, 5))
    self.make_move(move)
    if self.in_check(-self.turn_to_move):
        self.unmake_move(move)
        return False
    self.unmake_move(move)
    return True


def generate_moves(self):
    movelist = []
    direction_of_pawns = self.turn_to_move
    second_horizontal = 3 if direction_of_pawns == 1 else 8
    for i in range(2, 10):
        for j in range(2, 10):
            if color_of(self.board[i][j]) != self.turn_to_move:
                continue
            type_of_figure = type_of(self.board[i][j])
            if type_of_figure == KNIGHT:
                for k, l in moves_of_knight:
                    tmp = self.board[i + k][j + l]
                    if tmp == 0 or color_of(tmp) == -self.turn_to_move:
                        movelist.append(
                            Move((i, j), (i + k, j + l), broken=tmp))
            elif type_of_figure in (QUEEN, ROOK, BISHOP):
                directions = get_directions(type_of_figure)
                for k, l in directions:
                    for n in range(1, 10):
                        tmp = self.board[i + k * n][j + l * n]
                        if tmp != 0 and color_of(tmp) != -self.turn_to_move:
                            break
                        movelist.append(
                            Move((i, j), (i + k * n, j + l * n), broken=tmp))
                        if color_of(tmp) == -self.turn_to_move:
                            break
            elif type_of_figure == PAWN:
                if self.board[i + direction_of_pawns][j] == 0:
                    if i + direction_of_pawns in (2, 9):
                        for figure in (QUEEN, ROOK, BISHOP, KNIGHT):
                            movelist.append(Move((i, j),
                                                 (i + direction_of_pawns, j),
                                                 turn=figure * self.turn_to_move))
                    else:
                        movelist.append(
                            Move((i, j), (i + direction_of_pawns, j)))
                    if(i == second_horizontal and
                       self.board[i + 2 * direction_of_pawns][j] == 0):
                        movelist.append(
                            Move((i, j), (i + 2 * direction_of_pawns, j)))
                for k in (-1, 1):
                    tmp = self.board[i + direction_of_pawns][j + k]
                    if color_of(tmp) == -self.turn_to_move:
                        if i + direction_of_pawns in (2, 9):
                            for figure in (QUEEN, ROOK, BISHOP, KNIGHT):
                                movelist.append(Move((i, j),
                                                     (i + direction_of_pawns, j + k),
                                                     broken=tmp,
                                                     turn=figure * self.turn_to_move))
                        else:
                            movelist.append(Move((i, j),
                                                 (i + direction_of_pawns, j + k),
                                                 broken=tmp))
                    elif(self.en_passant == j + k and
                         i == second_horizontal + 3 * direction_of_pawns):
                        movelist.append(Move((i, j),
                                             (i + direction_of_pawns, j + k),
                                             broken=(
                                                 PAWN * -self.turn_to_move),
                                             en_passant=1))
            elif type_of_figure == KING:
                for k, l in moves_of_king:
                    tmp = self.board[i + k][j + l]
                    if tmp == 0 or color_of(tmp) == -self.turn_to_move:
                        movelist.append(Move((i, j),
                                             (i + k, j + l), broken=tmp))
                if castling_is_possible(self, i, 0):
                    movelist.append(Move((i, 6), (i, 8)))
                if castling_is_possible(self, i, 1):
                    movelist.append(Move((i, 6), (i, 4)))
    possible_moves = []
    for i in movelist:
        self.make_move(i)
        if not self.in_check(-self.turn_to_move):
            possible_moves.append(i)
        self.unmake_move(i)
    return possible_moves


def generate_captures(self):
    # some captures are ignored to make function simpler
    # a lot of copypaste from generate_moves
    # function added to make programm faster
    movelist = []
    direction_of_pawns = self.turn_to_move
    for i in range(2, 10):
        for j in range(2, 10):
            if color_of(self.board[i][j]) != self.turn_to_move:
                continue
            type_of_figure = type_of(self.board[i][j])
            if type_of_figure == KNIGHT:
                for k, l in moves_of_knight:
                    tmp = self.board[i + k][j + l]
                    if color_of(tmp) == -self.turn_to_move:
                        movelist.append(
                            Move((i, j), (i + k, j + l), broken=tmp))
            elif type_of_figure in (QUEEN, ROOK, BISHOP):
                directions = get_directions(type_of_figure)
                for k, l in directions:
                    for n in range(1, 10):
                        tmp = self.board[i + k * n][j + l * n]
                        if color_of(tmp) == -self.turn_to_move:
                            movelist.append(
                                Move((i, j), (i + k * n, j + l * n), broken=tmp))
                        if tmp != 0:
                            break
            elif type_of_figure == PAWN:
                for k in (-1, 1):
                    tmp = self.board[i + direction_of_pawns][j + k]
                    if color_of(tmp) == -self.turn_to_move:
                        turn = QUEEN if i + direction_of_pawns in (2, 9) else 0
                        movelist.append(Move((i, j), (i + direction_of_pawns, j + k),
                                             broken=tmp, turn=turn))
            elif type_of_figure == KING:
                for k, l in moves_of_king:
                    tmp = self.board[i + k][j + l]
                    if color_of(tmp) == -self.turn_to_move:
                        movelist.append(
                            Move((i, j), (i + k, j + l), broken=tmp))
    possible_moves = []
    for i in movelist:
        self.make_move(i)
        if not self.in_check(-self.turn_to_move):
            possible_moves.append(i)
        self.unmake_move(i)
    return possible_moves
