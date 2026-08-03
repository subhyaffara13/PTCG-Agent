import math


def alpha_pdf(x, a):
    if x > 0:
        return math.exp(-2.0 * math.log(x) - 0.5 * (a - 1.0 / x) ** 2)
    return 0.0

