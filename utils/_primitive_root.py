
def _primitive_root(p):
    """Compute a primitive root of the prime number `p`.

    Used in the CBC lattice construction.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Primitive_root_modulo_n
    """
    # p is prime
    pm = p - 1
    factors = _factorize_int(pm)
    n = len(factors)
    r = 2
    k = 0
    while k < n:
        d = pm // factors[k]
        # pow() doesn't like numpy scalar types.
        rd = pow(int(r), int(d), int(p))
        if rd == 1:
            r += 1
            k = 0
        else:
            k += 1
    return r

