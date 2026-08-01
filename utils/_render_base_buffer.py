
def _render_base_buffer(city: CityData) -> list[list[Color | None]]:
    buf: list[list[Color | None]] = [[None] * city.buf_w for _ in range(city.buf_h)]

    for tile in city.tiles:
        cx = city.x_off + (tile.grid_col - tile.grid_row) * _DX
        cy = city.y_off + (tile.grid_col + tile.grid_row) * _DY
        _draw_diamond_outline(buf, cx, cy)

    sorted_tiles = sorted(city.tiles, key=lambda t: (t.grid_row + t.grid_col, t.grid_col))
    for tile in sorted_tiles:
        cx = city.x_off + (tile.grid_col - tile.grid_row) * _DX
        cy = city.y_off + (tile.grid_col + tile.grid_row) * _DY
        _draw_block(buf, cx, cy, tile.height, tile.top, tile.left, tile.right)

    return buf

