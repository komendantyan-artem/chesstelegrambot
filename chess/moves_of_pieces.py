from piece_types import *

moves_of_knight = [(2, 1), (-2, 1), (2, -1), (-2, -1),
                   (1, 2), (-1, 2), (1, -2), (-1, -2)]
directions_of_bishop = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
directions_of_rook = [(1, 0), (-1, 0), (0, 1), (0, -1)]
directions_of_queen = directions_of_rook + directions_of_bishop
moves_of_king = directions_of_queen


def get_directions(piece):
    if type_of(piece) == BISHOP:
        return directions_of_bishop
    if type_of(piece) == ROOK:
        return directions_of_rook
    return directions_of_queen
