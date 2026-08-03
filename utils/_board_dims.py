from typing import Any

def _board_dims(state: Mapping[str, Any]) -> tuple[int, int]:
    """Return ``(num_rows, num_cols)`` from a parsed state dict.

    Prefers the actual board grid (always accurate), falls back to explicit
    dimension fields, and finally to a 10x10 default when the obs is empty.
    """
    board = state.get("board") or []
    if board:
        return len(board), len(board[0])
    nr = state.get("num_rows") or state.get("board_size") or _DEFAULT_BOARD_SIZE
    nc = state.get("num_cols") or state.get("board_size") or _DEFAULT_BOARD_SIZE
    return int(nr), int(nc)


def _board_dims(state: Mapping[str, Any]) -> tuple[int, int]:
    """Return ``(rows, columns)`` from a parsed state dict.

    Prefers the actual board grid (always accurate for the current state),
    falls back to the explicit ``rows``/``columns`` fields the proxy emits.
    Returns ``(0, 0)`` only when nothing is available.
    """
    board = state.get("board") or []
    if board:
        return len(board), len(board[0])
    rows = state.get("rows") or 0
    columns = state.get("columns") or 0
    return int(rows), int(columns)

