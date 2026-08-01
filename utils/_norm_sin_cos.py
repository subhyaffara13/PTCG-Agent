
def _normSinCos(v: float) -> float:
    if abs(v) < _EPSILON:
        v = 0
    elif v > _ONE_EPSILON:
        v = 1
    elif v < _MINUS_ONE_EPSILON:
        v = -1
    return v

