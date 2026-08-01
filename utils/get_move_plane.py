
def get_move_plane(move):
    source = move.from_square
    dest = move.to_square
    difference = diff(square_to_coord(source), square_to_coord(dest))

    QUEEN_MOVES = 56
    KNIGHT_MOVES = 8
    QUEEN_OFFSET = 0
    KNIGHT_OFFSET = QUEEN_MOVES
    UNDER_OFFSET = KNIGHT_OFFSET + KNIGHT_MOVES

    if is_knight_move(difference):
        return KNIGHT_OFFSET + get_knight_dir(difference)
    else:
        if move.promotion is not None and move.promotion != chess.QUEEN:
            return (
                UNDER_OFFSET
                + 3 * get_pawn_promotion_move(difference)
                + get_pawn_promotion_num(move.promotion)
            )
        else:
            return QUEEN_OFFSET + get_queen_plane(difference)

