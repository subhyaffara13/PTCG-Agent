
def get_pawn_promotion_num(promotion):
    assert (
        promotion == chess.KNIGHT
        or promotion == chess.BISHOP
        or promotion == chess.ROOK
    )
    return 0 if promotion == chess.KNIGHT else (1 if promotion == chess.BISHOP else 2)

