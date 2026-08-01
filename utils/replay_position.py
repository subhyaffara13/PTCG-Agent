
def replay_position(position, result):
    """Wrapper for a go.Position which replays its history.

    Assumes an empty start position! (i.e. no handicap, and history must be exhaustive.)

    Result must be passed in, since a resign cannot be inferred from position
    history alone.

    for position_w_context in replay_position(position):
        print(position_w_context.position)
    """
    assert position.n == len(position.recent), "Position history is incomplete"
    pos = Position(komi=position.komi)
    for player_move in position.recent:
        color, next_move = player_move
        yield PositionWithContext(pos, next_move, result)
        pos = pos.play_move(next_move, color=color)

