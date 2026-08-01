
def normalizeLinear(value, rangeMin, rangeMax):
    """Linearly normalize value in [rangeMin, rangeMax] to [0, 1], with extrapolation."""
    return (value - rangeMin) / (rangeMax - rangeMin)

