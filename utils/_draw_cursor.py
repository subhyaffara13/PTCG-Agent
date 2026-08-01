
def _draw_cursor(buf: list[list[Color | None]], cx: int, cy: int) -> None:
    bh = len(buf)
    bw = len(buf[0]) if buf else 0
    for dx, dy, color in _CURSOR_PIXELS:
        px, py = cx + dx, cy + dy
        if 0 <= py < bh and 0 <= px < bw:
            buf[py][px] = color

