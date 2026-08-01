
def _draw_block(
    buf: list[list[Color | None]],
    cx: int,
    cy: int,
    h: int,
    top: Color,
    left: Color,
    right: Color,
) -> None:
    _fill_poly(
        buf,
        [(cx - _DX, cy + _DY - h), (cx, cy + 2 * _DY - h), (cx, cy + 2 * _DY), (cx - _DX, cy + _DY)],
        left,
    )
    _fill_poly(
        buf,
        [(cx, cy + 2 * _DY - h), (cx + _DX, cy + _DY - h), (cx + _DX, cy + _DY), (cx, cy + 2 * _DY)],
        right,
    )
    _fill_poly(
        buf,
        [(cx, cy - h), (cx + _DX, cy + _DY - h), (cx, cy + 2 * _DY - h), (cx - _DX, cy + _DY - h)],
        top,
    )

