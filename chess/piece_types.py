BORDER = 100
EMPTY = 0
KING = 1
QUEEN = 2
ROOK = 3
BISHOP = 4
KNIGHT = 5
PAWN = 6
WHITE = 1
BLACK = -1

type_of = abs


def color_of(piece):
    if piece == 0 or piece == BORDER:
        return None
    return WHITE if piece > 0 else BLACK
