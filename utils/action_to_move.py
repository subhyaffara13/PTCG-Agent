
def action_to_move(board: chess.Board, action, player: int):
    base_move = chess.Move.from_uci(actions_to_moves[action])

    base_coord = square_to_coord(base_move.from_square)
    mirr_move = mirror_move(base_move) if player else base_move
    if mirr_move.promotion == chess.QUEEN:
        mirr_move.promotion = None
    if (
        mirr_move.promotion is None
        and str(board.piece_at(mirr_move.from_square)).lower() == "p"
        and base_coord[1] == 6
    ):
        mirr_move.promotion = chess.QUEEN
    return mirr_move

