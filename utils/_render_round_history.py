
def _render_round_history(
    round_history: list[list[str | None]] | None,
    num_players: int,
) -> str:
    """Render the per-round action log shared by all players.

    Lines are 1-indexed by round number, capped at the most recent
    ``_RECENT_ROUNDS_LIMIT`` rounds so the prompt doesn't grow without
    bound. ``None`` in a slot means the player didn't supply a move that
    round (e.g. they were already dead).
    """
    if not round_history:
        return "(no moves yet)"
    total = len(round_history)
    recent = round_history[-_RECENT_ROUNDS_LIMIT:]
    start_idx = total - len(recent) + 1
    lines = []
    for i, round_moves in enumerate(recent):
        round_num = start_idx + i
        parts = [
            f"P{p}={(round_moves[p] if p < len(round_moves) else None) or '-'}"
            for p in range(num_players)
        ]
        lines.append(f"Round {round_num}: " + ", ".join(parts))
    return "\n".join(lines)

