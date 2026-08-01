
def _xy(p):
    if isinstance(p, Planet):
        return p.x, p.y
    if isinstance(p, (list, tuple)):
        if len(p) >= 3 and isinstance(p[1], (int, float)) and isinstance(p[2], (int, float)):
            # [id, x, y, ...] form used in observations
            return p[1], p[2]
        return p[0], p[1]
    return p["x"], p["y"]

