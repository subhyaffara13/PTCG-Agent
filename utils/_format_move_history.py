from typing import Any

def _format_move_history(history: list[dict[str, Any]] | None) -> str:
    if not history:
        return "  (no moves yet)"
    tail = history[-_MOVE_HISTORY_TAIL:]
    return "\n".join(
        f"  move {idx + 1}: player {entry.get('player_id')} "
        f"(seat {entry.get('seat')}) -> {entry.get('action')}"
        for idx, entry in enumerate(tail, start=len(history) - len(tail))
    )


def _format_move_history(moves: Sequence[str]) -> str:
    return ", ".join(moves) if moves else "(none yet)"


def _format_move_history(move_history: list[str]) -> str:
    if not move_history:
        return "(no moves yet)"
    return ", ".join(move_history)


def _format_move_history(
    proxy_history: list[dict[str, Any]] | None,
    fallback: list[str],
) -> str:
    """Render the game-wide history if the proxy provides it, otherwise
    fall back to the per-agent history list supplied by core_harness.
    """
    if proxy_history:
        entries = [
            f"ant{int(entry.get('seat', 0))}:{entry.get('action', '?')}"
            for entry in proxy_history[-_MOVE_HISTORY_TAIL:]
        ]
        return ", ".join(entries) if entries else "None"
    if fallback:
        return ", ".join(fallback[-_MOVE_HISTORY_TAIL:])
    return "None"

