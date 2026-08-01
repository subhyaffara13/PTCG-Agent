
def phi_fixed(prec):
    """
    Computes the golden ratio, (1+sqrt(5))/2
    """
    prec += 10
    a = isqrt_fast(MPZ_FIVE<<(2*prec)) + (MPZ_ONE << prec)
    return a >> 11

