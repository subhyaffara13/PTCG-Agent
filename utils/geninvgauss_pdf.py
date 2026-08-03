import math


def geninvgauss_pdf(x, p, b):
    m = geninvgauss_mode(p, b)
    lfm = (p - 1) * math.log(m) - 0.5 * b * (m + 1 / m)
    if x > 0:
        return math.exp((p - 1) * math.log(x) - 0.5 * b * (x + 1 / x) - lfm)
    return 0.0

