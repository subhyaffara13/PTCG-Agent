
def get_pawn_promotion_move(diff):
    dx, dy = diff
    assert dy == 1
    assert -1 <= dx <= 1
    return dx + 1

