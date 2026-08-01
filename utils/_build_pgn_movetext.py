
def _build_pgn_movetext(state: pyspiel.State) -> str:
    """Build PGN movetext from a pyspiel chess state.

    Replicates the output of GameArena's ``format_chess_movetext`` with
    ``numbering_scheme="default"``, ``use_lan=False``, ``add_current_fen=False``.

    Format examples:
    - Empty game (White to play):  ``1.``
    - After 1. e4 (Black to play):  ``1. e4``
    - After 1. e4 e5 (White to play):  ``1. e4 e5 2.``
    - After 1. e4 e5 2. Nf3 (Black to play):  ``1. e4 e5 2. Nf3``

    A trailing move number is appended when it is White's turn, matching
    GameArena's behavior where the loop iterates ``range(len(nodes) + 1)``
    and adds the move number before checking for end-of-mainline.
    """
    history = state.history()
    game = state.get_game()
    tmp = game.new_initial_state()
    parts: list[str] = []

    for i, action in enumerate(history):
        if i % 2 == 0:
            # White's move — prepend move number
            parts.append(f"{i // 2 + 1}.")
        san = tmp.action_to_string(tmp.current_player(), action)
        parts.append(san)
        tmp.apply_action(action)

    # Trailing move number when it's White's turn (even number of moves).
    n = len(history)
    if n % 2 == 0:
        parts.append(f"{n // 2 + 1}.")

    return " ".join(parts)

