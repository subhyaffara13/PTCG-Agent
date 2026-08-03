import math


def wald_pdf(x):
    if x > 0:
        return math.exp(-((x - 1) ** 2) / (2 * x)) / math.sqrt(x**3)
    return 0.0

