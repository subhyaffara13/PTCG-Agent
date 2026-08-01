
def _format_ant_summary(
    ant_positions: list[list[int]],
    carrying_food: list[bool],
) -> str:
    if not ant_positions:
        return "  (none)"
    lines = []
    for i, pos in enumerate(ant_positions):
        carrying = bool(carrying_food[i]) if i < len(carrying_food) else False
        status = "carrying food" if carrying else "searching"
        lines.append(f"  ant {i}: at [{int(pos[0])},{int(pos[1])}], {status}")
    return "\n".join(lines)

