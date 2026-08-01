
def _format_board_ascii(board: Sequence[Sequence[str]]) -> str:
    """Render the board with rank labels on the left and files on top.

    The proxy returns ``board[0]`` as the top visual row (rank == rows),
    descending to ``board[rows-1]`` as rank 1. We print the rows in the
    same order so the visual orientation matches the proxy.
    """
    if not board:
        return "(unavailable)"
    rows = len(board)
    cols = len(board[0]) if board[0] else 0
    file_header = "  " + " ".join(chr(ord("a") + c) for c in range(cols))
    lines = [file_header]
    for r in range(rows):
        rank_label = rows - r
        lines.append(f"{rank_label:>2} " + " ".join(board[r]))
    return "\n".join(lines)


def _format_board_ascii(board: Sequence[Sequence[str]]) -> str:
    """Render the 8x8 board with rank labels on the left and files on top.

    ``board[0]`` is rank 1 (bottom row); ``board[7]`` is rank 8 (top). We
    print ranks top-down so the visual board matches standard orientation.
    """
    if not board:
        return "(unavailable)"
    file_header = "  " + " ".join(chr(ord("a") + c) for c in range(len(board[0])))
    lines = [file_header]
    for r in range(len(board) - 1, -1, -1):
        lines.append(f"{r + 1} " + " ".join(board[r]))
    return "\n".join(lines)


def _format_board_ascii(board: Sequence[Sequence[str]], rows: int, columns: int) -> str:
    """Render the board with rank labels on the left and file labels on top.

    Top row of ``board`` is the highest rank (top of the visual board); we
    label it ``rows`` and count down to 1 at the bottom.
    """
    if not board or not rows or not columns:
        return "(unavailable)"
    width = max(len(str(rows)), 1)
    lines = []
    file_header = " " * (width + 1) + " ".join(
        chr(ord("a") + c) for c in range(columns)
    )
    lines.append(file_header)
    for r, row in enumerate(board):
        rank_label = str(rows - r).rjust(width)
        lines.append(f"{rank_label} " + " ".join(row))
    return "\n".join(lines)


def _format_board_ascii(state: Mapping[str, Any]) -> str:
    """Render the board as an ASCII grid with edges and box owners.

    Rows of dots and horizontal edges interleave with rows of vertical
    edges and box cells. Open horizontal edges render as ``.`` and open
    vertical edges as ``:`` so the model can distinguish a candidate
    vertical edge from an unclaimed box (both sit in the same row);
    drawn edges show ``---`` / ``|``; box cells show the owning player
    digit or ``*`` for an unclaimed box.
    """
    num_rows = int(state.get("num_rows", 0))
    num_cols = int(state.get("num_cols", 0))
    h_lines = state.get("h_lines") or []
    v_lines = state.get("v_lines") or []
    boxes = state.get("boxes") or []
    if not (num_rows and num_cols and h_lines and v_lines):
        return "(unavailable)"

    lines: list[str] = []
    for r in range(num_rows + 1):
        # Dots + horizontal edges row.
        parts: list[str] = []
        for c in range(num_cols):
            parts.append("+")
            owner = h_lines[r][c] if r < len(h_lines) and c < len(h_lines[r]) else 0
            parts.append("---" if owner else " . ")
        parts.append("+")
        lines.append("".join(parts))

        if r >= num_rows:
            break

        # Vertical edges + box owners row.
        parts = []
        for c in range(num_cols + 1):
            owner = v_lines[r][c] if r < len(v_lines) and c < len(v_lines[r]) else 0
            parts.append("|" if owner else ":")
            if c < num_cols:
                box_owner = boxes[r][c] if r < len(boxes) and c < len(boxes[r]) else 0
                parts.append(f" {box_owner} " if box_owner else " * ")
        lines.append("".join(parts))

    return "\n".join(lines)


def _format_board_ascii(board: Sequence[Sequence[str]]) -> str:
    """Render the 8x8 board with rank labels on the left and files on top.

    ``board[0]`` is rank 1 (bottom row); ``board[7]`` is rank 8 (top). We
    print ranks top-down so the visual board matches standard orientation,
    and add row/column piece counts in the margins so the model doesn't
    have to count pieces on each line itself.
    """
    if not board:
        return "(unavailable)"
    n = len(board[0])
    file_header = "    " + " ".join(chr(ord("a") + c) for c in range(n)) + "   row"
    lines = [file_header]
    for r in range(len(board) - 1, -1, -1):
        row = board[r]
        row_count = sum(1 for cell in row if cell != ".")
        lines.append(f"  {r + 1} " + " ".join(row) + f"   {row_count}")
    col_counts = [
        sum(1 for r in range(len(board)) if board[r][c] != ".")
        for c in range(n)
    ]
    lines.append("col   " + " ".join(str(c) for c in col_counts))
    return "\n".join(lines)


def _format_board_ascii(board: list[list[str]], subgrid_winners: list[str], active_subgrid: int | None = None) -> str:
    """Format the 9x9 board into a 3x3 layout of 3x3 subgrids."""
    if not board:
        return "(board state unavailable)"

    sep = "      "
    lines = []
    # Loop over major rows (0, 1, 2)
    for major_row in range(3):
        # Header line for major row
        header_parts = []
        for mc in range(3):
            subgrid_idx = major_row * 3 + mc
            if active_subgrid == subgrid_idx:
                header_parts.append(f"> Local Board {subgrid_idx} <")
            else:
                header_parts.append(f"  Local Board {subgrid_idx}  ")
        lines.append(sep.join(header_parts))

        divider = sep.join("  +---+---+---+  " for _ in range(3))
        lines.append(divider)

        # Loop over minor rows (0, 1, 2)
        for minor_row in range(3):
            row_parts = []
            for major_col in range(3):
                subgrid_idx = major_row * 3 + major_col
                cells = []
                for minor_col in range(3):
                    cell_idx = minor_row * 3 + minor_col
                    char = board[subgrid_idx][cell_idx]
                    cells.append(char if char else ".")
                row_parts.append(f"{minor_row} | " + " | ".join(cells) + " |  ")
            lines.append(sep.join(row_parts))

        lines.append(divider)
        footer = sep.join("    0   1   2    " for _ in range(3))
        lines.append(footer)
        lines.append("")  # empty line between major rows

    # Add subgrid winners
    lines.append("Local Board Winners (overall 3x3 game):")
    for r in range(3):
        winners_row = []
        for c in range(3):
            idx = r * 3 + c
            w = subgrid_winners[idx]
            w_disp = f"[{w}]" if w else "[ ]"
            winners_row.append(f"{idx}: {w_disp}")
        lines.append("  ".join(winners_row))

    return "\n".join(lines)

