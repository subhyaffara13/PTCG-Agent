
def calculate_tiles_needed(
    resized_width,
    resized_height,
    tile_width=MAX_TILE_WIDTH,
    tile_height=MAX_TILE_HEIGHT,
):
    tiles_across = (resized_width + tile_width - 1) // tile_width
    tiles_down = (resized_height + tile_height - 1) // tile_height
    total_tiles = tiles_across * tiles_down
    return total_tiles

