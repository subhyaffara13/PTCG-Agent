
def _build_cursor() -> list[tuple[int, int, Color]]:
    pixels: list[tuple[int, int, Color]] = []
    for ri, row in enumerate(_CURSOR_GRID):
        for ci, ch in enumerate(row):
            if ch in _CURSOR_PALETTE:
                pixels.append((ci - len(row) // 2, ri - _CURSOR_H + 1, _CURSOR_PALETTE[ch]))
    return pixels

