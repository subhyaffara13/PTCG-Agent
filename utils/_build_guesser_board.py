
def _build_guesser_board(observation: Mapping[str, Any]) -> str:
    """Board state for Guesser (roles masked by the interpreter)."""
    words = observation.get("words", [])
    roles = observation.get("roles", [])
    revealed = observation.get("revealed", [])
    lines: list[str] = []
    for i in range(BOARD_SIZE):
        status = "Revealed" if revealed[i] else "Hidden"
        lines.append(f"- {i}: {words[i]} ({roles[i].upper()}, {status})")
    return "\n".join(lines)

