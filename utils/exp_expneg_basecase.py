
def exp_expneg_basecase(x, prec):
    """
    Computation of exp(x), exp(-x)
    """
    if prec > EXP_COSH_CUTOFF:
        cosh, sinh = exponential_series(x, prec, 1)
        return cosh+sinh, cosh-sinh
    a = exp_basecase(x, prec)
    b = (MPZ_ONE << (prec+prec)) // a
    return a, b

