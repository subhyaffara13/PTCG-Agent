
def _ordered_points(p):
    """Return the tuple of points sorted numerically according to args"""
    return tuple(sorted(p, key=lambda x: x.args))

