
def _opponent_archetype_signal(board_summary: dict[str, Any]) -> str | None:
    """Adjust strategy based on opponent's identified archetype."""
    arch = board_summary.get("opponent_archetype", "unknown")
    conf = board_summary.get("opponent_archetype_confidence", 0.0)
    if conf < 0.5 or arch == "unknown":
        return None
    raw_prizes = board_summary.get("prizes")
    if raw_prizes is None:
        raw_prizes = board_summary.get("my_prizes_remaining")
    prizes = int(raw_prizes) if raw_prizes is not None else 6
    if arch == "aggro" and prizes <= 4:
        return "disruption"  # Opponent is aggressive — disrupt hand and energy while building counter-push
    if arch == "stall" and prizes >= 4:
        return "aggro"  # Opponent stalls — pressure before they set up
    if arch == "combo" and prizes <= 4:
        return "aggro_push"  # Opponent is building combo — rush before it comes online
    if arch == "control":
        return "setup"  # Opponent controls — outvalue with more resources
    return None


def _opponent_archetype_signal(board_summary: dict[str, Any]) -> str | None:
    """Adjust strategy based on opponent's identified archetype."""
    arch = board_summary.get("opponent_archetype", "unknown")
    conf = board_summary.get("opponent_archetype_confidence", 0.0)
    if conf < 0.5 or arch == "unknown":
        return None
    raw_prizes = board_summary.get("prizes")
    if raw_prizes is None:
        raw_prizes = board_summary.get("my_prizes_remaining")
    prizes = int(raw_prizes) if raw_prizes is not None else 6
    if arch == "aggro" and prizes <= 4:
        return "disruption"  # Opponent is aggressive — disrupt hand and energy while building counter-push
    if arch == "stall" and prizes >= 4:
        return "aggro"  # Opponent stalls — pressure before they set up
    if arch == "combo" and prizes <= 4:
        return "aggro_push"  # Opponent is building combo — rush before it comes online
    if arch == "control":
        return "setup"  # Opponent controls — outvalue with more resources
    return None

