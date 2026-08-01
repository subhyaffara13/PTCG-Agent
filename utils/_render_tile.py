
def _render_tile(tile):
    if tile is None:
        return "."
    if tile == "LOCKED":
        return "#"
    if isinstance(tile, dict):
        kind = tile.get("kind")
        if kind == "WEED":
            return "x"
        if kind == "PLANT":
            return tile["crop"][0].lower()
        if "animal" in tile:
            return tile["animal"][0]
        if kind == "COOP":
            return "C"
        if kind == "PASTURE":
            return "P"
    return "?"

