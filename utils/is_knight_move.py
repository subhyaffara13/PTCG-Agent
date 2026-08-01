
def is_knight_move(diff):
    dx, dy = diff
    return abs(dx) + abs(dy) == 3 and 1 <= abs(dx) <= 2

