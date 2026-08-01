
def _is_mid_point(p0: tuple, p1: tuple, p2: tuple) -> bool:
    # True if p1 is in the middle of p0 and p2, either before or after rounding
    p0 = Vector(p0)
    p1 = Vector(p1)
    p2 = Vector(p2)
    return ((p0 + p2) * 0.5).isclose(p1) or _roundv(p0) + _roundv(p2) == _roundv(p1) * 2

