
def mpf_loggamma(x, prec, rnd='d'):
    sign, man, exp, bc = x
    if sign:
        raise ComplexResult
    return mpf_gamma(x, prec, rnd, 3)

