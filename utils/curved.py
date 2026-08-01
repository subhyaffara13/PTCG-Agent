
def curved(middle: float, pos: float) -> float:
    return pos ** (log(0.5) / log(max(middle, EPSILON)))

