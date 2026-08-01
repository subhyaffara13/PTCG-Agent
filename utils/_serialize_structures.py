
def _serialize_structures(game):
    """Convert capturable structures to a list of dicts.

    ``regenerating`` is the engine flag flipped on by
    ``mechanics.regenerate_structures`` (and on attacker/defender tile
    after a death) -- without it the replay would see structure HP
    snap upward at end of turn with no in-band explanation.
    """
    structures = []
    for row in game.grid.tiles:
        for tile in row:
            if tile.is_capturable():
                structures.append(
                    {
                        "x": tile.x,
                        "y": tile.y,
                        "type": tile.type,
                        "owner": tile.player if tile.player else 0,
                        "hp": tile.health if tile.health is not None else 0,
                        "maxHp": tile.max_health if tile.max_health is not None else 0,
                        "regenerating": bool(getattr(tile, "regenerating", False)),
                    }
                )
    return structures

