
def _highlight_tile(buf: list[list[Color | None]], city: CityData, tile: TileInfo) -> None:
    cx = city.x_off + (tile.grid_col - tile.grid_row) * _DX
    cy = city.y_off + (tile.grid_col + tile.grid_row) * _DY
    h = tile.height
    _fill_poly(
        buf,
        [(cx, cy - h), (cx + _DX, cy + _DY - h), (cx, cy + 2 * _DY - h), (cx - _DX, cy + _DY - h)],
        _brighten(tile.top, 35),
    )

