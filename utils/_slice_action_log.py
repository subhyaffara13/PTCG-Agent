
def _slice_action_log(game, start_idx):
    """Return engine action_history entries appended this turn.

    Strips the per-entry wall-clock ``timestamp`` (verbose ISO datetime
    that bloats the replay JSON and isn't needed to reconstruct game
    state) and recursively converts any tuples (today: coordinate pairs
    like ``position``/``attacker_pos``; future-proof against nested
    structures like paths or value-lists) to lists so the result
    round-trips cleanly through JSON without relying on stdlib json's
    tuple-as-array coercion.
    """
    entries = []
    for entry in game.action_history[start_idx:]:
        record = {}
        for key, value in entry.items():
            if key == "timestamp":
                continue
            record[key] = _normalize_for_json(value)
        entries.append(record)
    return entries

