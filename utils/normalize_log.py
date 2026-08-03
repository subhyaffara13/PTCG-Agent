import math


def normalizeLog(value, rangeMin, rangeMax):
    """Logarithmically normalize value in [rangeMin, rangeMax] to [0, 1], with extrapolation."""
    logMin = math.log(rangeMin)
    logMax = math.log(rangeMax)
    return (math.log(value) - logMin) / (logMax - logMin)

