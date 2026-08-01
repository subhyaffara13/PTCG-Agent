
def get_visible_cells(robots, config):
    """Return set of (col, row) tuples visible to a player's robots."""
    visible = set()
    for r in robots:
        v = get_vision(r["type"], config)
        rc, rr = r["col"], r["row"]
        for dc in range(-v, v + 1):
            for dr in range(-v, v + 1):
                if abs(dc) + abs(dr) <= v:
                    c = rc + dc
                    if 0 <= c < config.width:
                        visible.add((c, rr + dr))
    return visible

