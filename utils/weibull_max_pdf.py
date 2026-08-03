import math


def weibull_max_pdf(x, c):
    if x < 0:
        return c * math.exp((c - 1) * math.log(-x) - ((-x) ** c))
    return 0.0

