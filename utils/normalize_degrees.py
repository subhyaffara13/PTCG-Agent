
def normalizeDegrees(value, rangeMin, rangeMax):
    """Angularly normalize value in [rangeMin, rangeMax] to [0, 1], with extrapolation."""
    tanMin = math.tan(math.radians(rangeMin))
    tanMax = math.tan(math.radians(rangeMax))
    return (math.tan(math.radians(value)) - tanMin) / (tanMax - tanMin)

