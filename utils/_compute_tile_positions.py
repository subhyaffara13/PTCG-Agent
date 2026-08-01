
def _compute_tile_positions(moves: list[str]) -> dict[str, list[int]]:
    """Replay moves to compute current (q, r, h) for each played tile."""
    positions: dict[str, list[int]] = {}
    for move_str in moves:
        from_tile, ref_tile, direction = _parse_uhp_move(move_str)
        if from_tile == "pass":
            continue
        if ref_tile is None:
            positions[from_tile] = [0, 0, 0]
            continue
        ref_pos = positions.get(ref_tile)
        if ref_pos is None:
            # Shouldn't happen for a valid game; skip rather than crash.
            continue
        ref_q, ref_r, ref_h = ref_pos
        if direction == "Above":
            new_q, new_r, new_h = ref_q, ref_r, ref_h + 1
        else:
            dq, dr = _DIRECTION_OFFSETS[direction]
            new_q, new_r = ref_q + dq, ref_r + dr
            max_h = -1
            for tile, (q, r, h) in positions.items():
                if tile == from_tile:
                    continue
                if q == new_q and r == new_r and h > max_h:
                    max_h = h
            new_h = max_h + 1
        positions[from_tile] = [new_q, new_r, new_h]
    return positions

