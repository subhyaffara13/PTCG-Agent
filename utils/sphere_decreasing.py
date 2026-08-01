
def sphere_decreasing(middle: float, pos: float) -> float:
    return 1.0 - sqrt(1.0 - linear(middle, pos) ** 2)

