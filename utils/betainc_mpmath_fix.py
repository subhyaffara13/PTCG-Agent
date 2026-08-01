
def betainc_mpmath_fix(a, b, x1, x2, reg=0):
    from mpmath import betainc, mpf
    if x1 == x2:
        return mpf(0)
    else:
        return betainc(a, b, x1, x2, reg)

