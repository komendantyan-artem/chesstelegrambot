class Move:
    def __init__(self, start, to, broken=0, en_passant=0, turn=0):
        self.start = start
        self.to = to
        self.broken = broken
        self.en_passant = en_passant
        self.turn = turn
        self.copies_of_flags = None


def captures_in_begin(move):
    return not move.broken
