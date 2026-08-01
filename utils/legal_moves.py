
def legal_moves(orig_board: chess.Board):
    """Returns legal moves.

    action space is a 8x8x73 dimensional array
    Each of the 8×8
    positions identifies the square from which to “pick up” a piece. The first 56 planes encode
    possible ‘queen moves’ for any piece: a number of squares [1..7] in which the piece will be
    moved, along one of eight relative compass directions {N, NE, E, SE, S, SW, W, NW}. The
    next 8 planes encode possible knight moves for that piece. The final 9 planes encode possible
    underpromotions for pawn moves or captures in two possible diagonals, to knight, bishop or
    rook respectively. Other pawn moves or captures from the seventh rank are promoted to a
    queen
    """
    if orig_board.turn == chess.BLACK:  # white is 1, black is 0
        board = orig_board.mirror()
    else:
        board = orig_board

    legal_moves = []
    for move in board.legal_moves:
        uci_move = move.uci()
        if uci_move in moves_to_actions:
            legal_moves.append(moves_to_actions[move.uci()])
        else:
            make_move_mapping(uci_move)
            legal_moves.append(moves_to_actions[move.uci()])

    return legal_moves

