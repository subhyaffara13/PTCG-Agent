from typing import Any

def _render_board(board: Sequence[Sequence[str]]) -> str:
    """Render the board with column letters and row numbers around the edges."""
    rows_count = len(board)
    cols_count = len(board[0]) if rows_count else 0
    header = "   " + " ".join(string.ascii_lowercase[:cols_count])
    rows: list[str] = [header]
    for r in range(rows_count):
        rows.append(f"{r + 1:>2} " + " ".join(board[r]))
    return "\n".join(rows)


def _render_board(board: Any) -> str:
    """Render the proxy's board (list of rows of single-char cells) as ASCII."""
    if not isinstance(board, list) or not board:
        return "(board unavailable)"
    return "\n".join("".join(row) for row in board)


def _render_board(board: list[list[str]], num_cols: int) -> str:
    """Render the hex board with column letters, row numbers, and indentation.

    Each row is shifted half a cell to the right of the row above, mirroring
    the parallelogram layout of a Hex grid.
    """
    if not board:
        return "(board unavailable)"
    col_header = "    " + " ".join(chr(ord("a") + c) for c in range(num_cols))
    lines = [col_header]
    for r, row in enumerate(board):
        indent = " " * r
        cells = " ".join(row)
        lines.append(f"{indent}{r + 1:>2}  {cells}")
    return "\n".join(lines)


def _render_board(parsed: Mapping[str, Any]) -> str:
    """Render the proxy's JSON board as the human-readable ASCII grid.

    Mirrors the OpenSpiel ToString() layout so the prompt matches the coordinate
    conventions players already know.
    """
    board = parsed.get("board") or []
    board_size = int(parsed.get("board_size") or len(board) // 2 + 1)
    diameter = board_size * 2 - 1

    lines: list[str] = []
    # Top column labels: a..<letter at board_size-1>
    top_indent = " " * (board_size + 3)
    top_labels = " ".join(chr(ord("a") + x) for x in range(board_size))
    lines.append(f"{top_indent} {top_labels}")

    for y in range(diameter):
        row_cells = board[y] if y < len(board) else []
        glyphs = []
        for cell in row_cells:
            if cell == "x":
                glyphs.append("X")
            elif cell == "o":
                glyphs.append("O")
            else:
                glyphs.append(".")
        leading_spaces = abs(board_size - 1 - y) + 1 + (0 if y + 1 >= 10 else 1)
        prefix = " " * leading_spaces + str(y + 1)
        body = " " + " ".join(glyphs)
        if y < board_size - 1:
            # Trailing right-column label, matching the OpenSpiel layout.
            suffix = " " + chr(ord("a") + board_size + y)
            lines.append(prefix + body + suffix)
        else:
            lines.append(prefix + body)
    return "\n".join(lines) + "\n"


def _render_board(board: list[list[str]] | None) -> str:
    """Render the proxy's 2D board array as a single ASCII grid."""
    if not board:
        return "(no board)"
    return "\n".join("".join(row) for row in board)

