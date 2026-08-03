import math


def argus_pdf(x, chi):
    # approach follows Baumgarten/Hoermann: Generating ARGUS random variates
    # for chi > 5, use relationship of the ARGUS distribution to Gamma(1.5)
    if chi <= 5:
        y = 1 - x * x
        return x * math.sqrt(y) * math.exp(-0.5 * chi**2 * y)
    return math.sqrt(x) * math.exp(-x)

