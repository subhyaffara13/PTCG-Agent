
def _build_cluemaster_board(observation: Mapping[str, Any]) -> str:
    """Board state for Cluemaster (full visibility)."""
    words = observation.get("words", [])
    roles = observation.get("roles", [])
    revealed = observation.get("revealed", [])
    lines: list[str] = []
    for i in range(BOARD_SIZE):
        status = "Revealed" if revealed[i] else "Hidden"
        lines.append(f"- {words[i]}: {roles[i].upper()} ({status})")
    return "\n".join(lines)

