
def _format_state(observation: Mapping[str, Any]) -> tuple[str, int]:
    """Format the observation as an ASCII board plus return the board size."""
    raw = observation.get("observationString", "")
    if not raw:
        return "", 0
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        # Fall back to the raw string if it isn't JSON.
        return raw if raw.endswith("\n") else raw + "\n", 0
    board_size = int(parsed.get("board_size") or 0)
    return _render_board(parsed), board_size

