
def _render_move_history(history: Any) -> str:
    """Render the per-board move log; arena-style annotated lines."""
    if not history:
        return "  (no moves yet)"
    return "\n".join(
        f"  move {entry.get('move_number')}: player {entry.get('player_id')} -> {entry.get('action')}"
        for entry in history
    )

