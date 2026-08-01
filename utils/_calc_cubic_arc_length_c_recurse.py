
def _calcCubicArcLengthCRecurse(mult, p0, p1, p2, p3):
    arch = abs(p0 - p3)
    box = abs(p0 - p1) + abs(p1 - p2) + abs(p2 - p3)
    if arch * mult + EPSILON >= box:
        return (arch + box) * 0.5
    else:
        one, two = _split_cubic_into_two(p0, p1, p2, p3)
        return _calcCubicArcLengthCRecurse(mult, *one) + _calcCubicArcLengthCRecurse(
            mult, *two
        )

