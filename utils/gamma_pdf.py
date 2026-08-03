import math


def gamma_pdf(x, a):
    if x > 0:
        return math.exp(-math.lgamma(a) + (a - 1.0) * math.log(x) - x)
    else:
        return 0 if a >= 1 else np.inf

