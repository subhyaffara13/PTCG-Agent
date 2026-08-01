
def _draw_diamond_outline(buf: list[list[Color | None]], cx: int, cy: int) -> None:
    t = (cx, cy)
    r = (cx + _DX, cy + _DY)
    b = (cx, cy + 2 * _DY)
    ll = (cx - _DX, cy + _DY)
    _draw_line(buf, *t, *r, _GRID_COLOR)
    _draw_line(buf, *r, *b, _GRID_COLOR)
    _draw_line(buf, *b, *ll, _GRID_COLOR)
    _draw_line(buf, *ll, *t, _GRID_COLOR)

