
def _render_grid_ascii(
    grid: list[list[str]],
    ant_positions_by_pid: Mapping[str, Any] | None,
    carrying_by_pid: Mapping[str, Any] | None,
    players_per_team: int,
    team_id: int,
) -> str:
    """Render the team board with the team's ants overlaid on terrain.

    First-seat-wins when multiple ants share a cell (matches upstream
    ant_foraging's __str__ convention). The prose elsewhere lists each
    ant's position separately, so any stacking lost here is recoverable.
    """
    rows = len(grid) if grid else 0
    cols = len(grid[0]) if rows else 0
    ant_positions_by_pid = ant_positions_by_pid or {}
    carrying_by_pid = carrying_by_pid or {}

    # Seat -> (row, col) using team-relative seat indices so the renderer
    # stays symmetric across the two teams.
    seat_at: dict[tuple[int, int], int] = {}
    for seat in range(players_per_team):
        pid = team_id * players_per_team + seat
        pos = ant_positions_by_pid.get(str(pid))
        if not pos or len(pos) < 2:
            continue
        cell = (int(pos[0]), int(pos[1]))
        if cell not in seat_at:
            seat_at[cell] = seat

    header = "    " + " ".join(str(c) for c in range(cols))
    lines = [header]
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            if (r, c) in seat_at:
                seat = seat_at[(r, c)]
                pid = team_id * players_per_team + seat
                carrying = bool(carrying_by_pid.get(str(pid), False))
                row_chars.append(_ant_glyph(seat, carrying))
            else:
                row_chars.append(grid[r][c])
        lines.append(f"{r:>2}  " + " ".join(row_chars))
    return "\n".join(lines)


def _render_grid_ascii(
    grid: list[list[str]],
    ant_positions: list[list[int]],
    carrying_food: list[bool],
) -> str:
    """Render the board with ants overlaid on terrain.

    First-ant-wins when multiple ants share a cell (matches the engine's
    own __str__). The prose elsewhere in the prompt lists every ant's
    position separately, so any stacking lost here is recoverable.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    ant_at: dict[tuple[int, int], int] = {}
    for i, pos in enumerate(ant_positions):
        if not pos or len(pos) < 2:
            continue
        cell = (int(pos[0]), int(pos[1]))
        if cell not in ant_at:
            ant_at[cell] = i

    header = "    " + " ".join(str(c) for c in range(cols))
    lines = [header]
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            if (r, c) in ant_at:
                i = ant_at[(r, c)]
                carrying = bool(carrying_food[i]) if i < len(carrying_food) else False
                row_chars.append(_ant_glyph(i, carrying))
            else:
                row_chars.append(grid[r][c])
        lines.append(f"{r:>2}  " + " ".join(row_chars))
    return "\n".join(lines)

