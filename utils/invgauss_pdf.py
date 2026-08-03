import math


def invgauss_pdf(x, mu):
    m = invgauss_mode(mu)
    lfm = -1.5 * math.log(m) - (m - mu) ** 2 / (2 * m * mu**2)
    if x > 0:
        return math.exp(-1.5 * math.log(x) - (x - mu) ** 2 / (2 * x * mu**2) - lfm)
    return 0.0

