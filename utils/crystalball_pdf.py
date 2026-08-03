import math


def crystalball_pdf(x, b, m):
    if x > -b:
        return math.exp(-0.5 * x * x)
    return math.exp(m * math.log(m / b) - 0.5 * b * b - m * math.log(m / b - b - x))

