
def sphere_increasing(middle: float, pos: float) -> float:
    return sqrt(1.0 - (linear(middle, pos) - 1.0) ** 2)

