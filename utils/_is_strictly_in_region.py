
def _is_strictly_in_region(a, b, point, xp):
    if xp.all(point == a) or xp.all(point == b):
        return False

    return xp.all(a <= point) and xp.all(point <= b)

