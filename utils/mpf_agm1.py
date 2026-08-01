
def mpf_agm1(a, prec, rnd=round_fast):
    """
    Computes the arithmetic-geometric mean agm(1,a) for a nonnegative
    mpf value a.
    """
    return mpf_agm(fone, a, prec, rnd)

