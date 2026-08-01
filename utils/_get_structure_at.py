
def _get_structure_at(structures, x, y):
    """Find a structure at the given position."""
    for s in structures:
        if s["x"] == x and s["y"] == y:
            return s
    return None

