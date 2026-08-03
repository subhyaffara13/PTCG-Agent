import math


def invgamma_pdf(x, a):
    if x > 0:
        return math.exp(-(a + 1.0) * math.log(x) - math.lgamma(a) - 1 / x)
    else:
        return 0 if a >= 1 else np.inf

