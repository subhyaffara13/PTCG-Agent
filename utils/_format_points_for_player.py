
def _format_points_for_player(
    board: Sequence[Mapping[str, Any] | None],
    player_id: int,
    want_label: str,
) -> str:
    """Render occupied points (for one side) in player-relative numbering."""
    entries: list[tuple[int, int]] = []  # (player_point, count)
    for abs_pos, slot in enumerate(board):
        if not slot:
            continue
        if slot.get("player") != want_label:
            continue
        point = _abs_to_point(player_id, abs_pos)
        entries.append((point, int(slot.get("count", 0))))
    if not entries:
        return "  (none on the board)"
    entries.sort(key=lambda t: -t[0])  # high to low, matches play order
    return "\n".join(f"  point {pt:>2}: {ct}" for pt, ct in entries)

