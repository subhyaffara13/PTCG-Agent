
def _tile_top_center(city: CityData, row: int, col: int, tile_map: dict[tuple[int, int], TileInfo]) -> tuple[int, int]:
    tile = tile_map.get((row, col))
    h = tile.height if tile else 1
    cx = city.x_off + (col - row) * _DX
    cy = city.y_off + (col + row) * _DY
    return cx, cy + _DY - h

