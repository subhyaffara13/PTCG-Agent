import math


def interpolateLog(t, a, b):
    """Logarithmic interpolation between a and b, with t typically in [0, 1]."""
    logA = math.log(a)
    logB = math.log(b)
    return math.exp(logA + t * (logB - logA))

