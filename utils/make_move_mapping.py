
def make_move_mapping(uci_move):
    TOTAL = 73
    move = chess.Move.from_uci(uci_move)
    source = move.from_square

    coord = square_to_coord(source)
    panel = get_move_plane(move)
    cur_action = (coord[0] * 8 + coord[1]) * TOTAL + panel

    moves_to_actions[uci_move] = cur_action
    actions_to_moves[cur_action] = uci_move

